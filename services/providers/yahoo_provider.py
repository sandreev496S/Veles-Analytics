from datetime import datetime, timezone
from typing import Any, Dict

try:
    import yfinance as yf
except ModuleNotFoundError:  # optional for deterministic unit/integration tests
    yf = None

from services.providers.base_provider import BaseProvider
from services.providers.yahoo_raw import (
    get_latest_raw_statement_value,
    get_raw_statement_series,
    safe_number,
)


def _safe(value: Any, default: str = "N/A") -> Any:
    if value is None or value == "":
        return default
    return value


def _fmt_money(value: Any) -> str:
    if value is None:
        return "N/A"
    try:
        value = float(value)
        if abs(value) >= 1_000_000_000:
            return f"${value / 1_000_000_000:.2f}B"
        if abs(value) >= 1_000_000:
            return f"${value / 1_000_000:.2f}M"
        return f"${value:,.2f}"
    except Exception:
        return "N/A"


def _fmt_num(value: Any) -> str:
    if value is None:
        return "N/A"
    try:
        value = float(value)
        if abs(value) >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"
        if abs(value) >= 1_000:
            return f"{value / 1_000:.2f}K"
        return f"{value:,.2f}"
    except Exception:
        return "N/A"


def _get_statement_row(df: Any, row_name: str, max_periods: int = 3) -> list[str]:
    try:
        if df is None or getattr(df, "empty", True):
            return ["N/A"] * max_periods

        aliases = {
            "Total Revenue": (
                "Total Revenue",
                "Operating Revenue",
                "Revenue",
            ),
            "Research And Development": (
                "Research And Development",
                "Research Development",
            ),
            "Operating Income": (
                "Operating Income",
                "Operating Income Loss",
            ),
            "Net Income": (
                "Net Income",
                "Net Income Common Stockholders",
                "Net Income Including Noncontrolling Interests",
            ),
            "Cash And Cash Equivalents": (
                "Cash And Cash Equivalents",
                "Cash Cash Equivalents And Short Term Investments",
                "Cash Financial",
            ),
            "Total Debt": (
                "Total Debt",
                "Long Term Debt And Capital Lease Obligation",
                "Long Term Debt",
            ),
            "Stockholders Equity": (
                "Stockholders Equity",
                "Common Stock Equity",
                "Total Equity Gross Minority Interest",
            ),
            "Operating Cash Flow": (
                "Operating Cash Flow",
                "Cash Flow From Continuing Operating Activities",
            ),
            "Capital Expenditure": (
                "Capital Expenditure",
                "Capital Expenditures",
            ),
            "Free Cash Flow": (
                "Free Cash Flow",
            ),
        }

        def normalize(value):
            return "".join(
                character.lower()
                for character in str(value)
                if character.isalnum()
            )

        index_lookup = {
            normalize(index): index
            for index in df.index
        }

        resolved_row = None
        for alias in aliases.get(row_name, (row_name,)):
            resolved_row = index_lookup.get(normalize(alias))
            if resolved_row is not None:
                break

        if resolved_row is None:
            return ["N/A"] * max_periods

        values = []
        for col in list(df.columns)[:max_periods]:
            values.append(_fmt_money(df.loc[resolved_row, col]))

        while len(values) < max_periods:
            values.append("N/A")

        return values
    except Exception:
        return ["N/A"] * max_periods


def _period_labels(df: Any, max_periods: int = 3) -> list[str]:
    try:
        labels = []
        for col in list(df.columns)[:max_periods]:
            labels.append(str(col.date()) if hasattr(col, "date") else str(col))

        while len(labels) < max_periods:
            labels.append("N/A")

        return labels
    except Exception:
        return ["N/A"] * max_periods


class YahooProvider(BaseProvider):
    name = "yfinance"
    capabilities = {"company", "financials", "market"}

    def __init__(self) -> None:
        pass

    def health_check(self) -> Dict[str, Any]:
        if yf is None:
            return {
                "provider": self.name,
                "status": "unavailable",
                "note": "Install the optional yfinance dependency to use live Yahoo Finance data.",
            }
        return {
            "provider": self.name,
            "status": "online",
            "note": "Yahoo Finance provider available through yfinance import.",
        }

    def _ticker(self, ticker: str):
        if yf is None:
            raise RuntimeError(
                "YahooProvider requires the optional 'yfinance' package for live data. "
                "Install project requirements or use a fixture-backed provider in tests."
            )
        return yf.Ticker(ticker.upper().strip())

    def get_company_data(self, ticker: str) -> Dict[str, Any]:
        ticker = ticker.upper().strip()
        stock = self._ticker(ticker)

        try:
            info = stock.info or {}
        except Exception:
            info = {}

        company_name = _safe(info.get("longName"), ticker)
        city = _safe(info.get("city"), "")
        state = _safe(info.get("state"), "")
        country = _safe(info.get("country"), "")
        headquarters = ", ".join([x for x in [city, state, country] if x and x != "N/A"]) or "N/A"

        return {
            "company_name": company_name,
            "ticker": ticker,
            "exchange": _safe(info.get("exchange")),
            "industry": _safe(info.get("industry")),
            "sector": _safe(info.get("sector")),
            "website": _safe(info.get("website")),
            "headquarters": headquarters,
            "business_model": _safe(info.get("longBusinessSummary"), "Business model data unavailable."),
            "description": _safe(info.get("longBusinessSummary"), "Company description unavailable."),
            "ceo": "N/A",
            "founded": "N/A",
            "report_view": "Auto-generated from Yahoo Finance provider",
            "stage": "Public company",
        }

    def get_market_data(self, ticker: str) -> Dict[str, Any]:
        ticker = ticker.upper().strip()
        stock = self._ticker(ticker)

        try:
            info = stock.info or {}
        except Exception:
            info = {}

        retrieved_at = datetime.now(
            timezone.utc
        ).isoformat(timespec="seconds")

        raw_metrics = {
            "share_price": {
                "value": safe_number(
                    info.get("currentPrice")
                    or info.get("regularMarketPrice")
                ),
                "unit": info.get("currency", "USD"),
                "definition": (
                    "Latest price reported by Yahoo Finance."
                ),
            },
            "market_cap": {
                "value": safe_number(info.get("marketCap")),
                "unit": info.get("currency", "USD"),
                "definition": (
                    "Provider-reported equity market "
                    "capitalization."
                ),
            },
            "provider_enterprise_value": {
                "value": safe_number(
                    info.get("enterpriseValue")
                ),
                "unit": info.get("currency", "USD"),
                "definition": (
                    "Enterprise value calculated by Yahoo "
                    "Finance using provider-defined inputs."
                ),
            },
            "fifty_two_week_high": {
                "value": safe_number(
                    info.get("fiftyTwoWeekHigh")
                ),
                "unit": info.get("currency", "USD"),
            },
            "fifty_two_week_low": {
                "value": safe_number(
                    info.get("fiftyTwoWeekLow")
                ),
                "unit": info.get("currency", "USD"),
            },
            "beta": {
                "value": safe_number(info.get("beta")),
                "unit": "ratio",
            },
            "average_volume": {
                "value": safe_number(
                    info.get("averageVolume")
                ),
                "unit": "shares",
            },
        }

        return {
            "currency": info.get("currency", "USD"),
            "as_of": retrieved_at,
            "provider": self.name,
            "raw_metrics": raw_metrics,
            "market_snapshot": [
                ["Metric", "Value"],
                ["Share Price", _fmt_money(info.get("currentPrice") or info.get("regularMarketPrice"))],
                ["Market Cap", _fmt_money(info.get("marketCap"))],
                ["Enterprise Value", _fmt_money(info.get("enterpriseValue"))],
                ["52-Week High", _fmt_money(info.get("fiftyTwoWeekHigh"))],
                ["52-Week Low", _fmt_money(info.get("fiftyTwoWeekLow"))],
                ["Beta", _fmt_num(info.get("beta"))],
                ["Average Volume", _fmt_num(info.get("averageVolume"))],
            ],
            "valuation_multiples": [
                ["Metric", "Value"],
                ["EV / Revenue", _fmt_num(info.get("enterpriseToRevenue"))],
                ["Price / Sales", _fmt_num(info.get("priceToSalesTrailing12Months"))],
                ["Forward P/E", _fmt_num(info.get("forwardPE"))],
                ["Price / Book", _fmt_num(info.get("priceToBook"))],
            ],
            "market_commentary": [
                f"Market data pulled using Yahoo Finance provider for {ticker}.",
                "Interpret valuation multiples against growth, margins, capital intensity, and comparable companies.",
            ],
        }

    def get_financial_data(self, ticker: str) -> Dict[str, Any]:
        ticker = ticker.upper().strip()
        stock = self._ticker(ticker)

        errors = []

        try:
            income = stock.get_income_stmt(
                freq="yearly",
                pretty=True,
            )
            if income is None or income.empty:
                income = stock.income_stmt
        except Exception as exc:
            errors.append(f"income statement: {exc}")
            try:
                income = stock.income_stmt
            except Exception:
                income = None

        try:
            balance = stock.get_balance_sheet(
                freq="yearly",
                pretty=True,
            )
            if balance is None or balance.empty:
                balance = stock.balance_sheet
        except Exception as exc:
            errors.append(f"balance sheet: {exc}")
            try:
                balance = stock.balance_sheet
            except Exception:
                balance = None

        try:
            cashflow = stock.get_cash_flow(
                freq="yearly",
                pretty=True,
            )
            if cashflow is None or cashflow.empty:
                cashflow = stock.cashflow
        except Exception as exc:
            errors.append(f"cash-flow statement: {exc}")
            try:
                cashflow = stock.cashflow
            except Exception:
                cashflow = None

        if not any(
            statement is not None
            and not getattr(statement, "empty", True)
            for statement in (income, balance, cashflow)
        ):
            details = "; ".join(errors) or "empty Yahoo response"
            raise RuntimeError(
                f"Yahoo returned no financial statements for "
                f"{ticker}: {details}"
            )

        periods = _period_labels(income)

        raw_metrics = {
            "total_revenue": {
                "observations": get_raw_statement_series(
                    income,
                    "Total Revenue",
                ),
                "unit": "USD",
                "taxonomy": "provider_total_revenue",
                "definition": (
                    "Yahoo Finance row named Total Revenue. "
                    "Underlying accounting composition must "
                    "be reconciled against SEC filings."
                ),
            },
            "research_and_development_expense": {
                "observations": get_raw_statement_series(
                    income,
                    "Research And Development",
                ),
                "unit": "USD",
                "taxonomy": (
                    "research_and_development_expense"
                ),
            },
            "operating_income": {
                "observations": get_raw_statement_series(
                    income,
                    "Operating Income",
                ),
                "unit": "USD",
                "taxonomy": "operating_income_loss",
            },
            "net_income": {
                "observations": get_raw_statement_series(
                    income,
                    "Net Income",
                ),
                "unit": "USD",
                "taxonomy": "net_income_loss",
            },
            "cash_and_cash_equivalents": {
                **get_latest_raw_statement_value(
                    balance,
                    "Cash And Cash Equivalents",
                ),
                "unit": "USD",
                "taxonomy": (
                    "cash_and_cash_equivalents"
                ),
            },
            "provider_total_debt": {
                **get_latest_raw_statement_value(
                    balance,
                    "Total Debt",
                ),
                "unit": "USD",
                "taxonomy": "provider_total_debt",
                "definition": (
                    "Yahoo Finance Total Debt. Components "
                    "and lease treatment are not guaranteed "
                    "and require reconciliation."
                ),
            },
            "stockholders_equity": {
                **get_latest_raw_statement_value(
                    balance,
                    "Stockholders Equity",
                ),
                "unit": "USD",
                "taxonomy": "stockholders_equity",
            },
            "operating_cash_flow": {
                **get_latest_raw_statement_value(
                    cashflow,
                    "Operating Cash Flow",
                ),
                "unit": "USD",
                "taxonomy": "operating_cash_flow",
            },
            "capital_expenditure": {
                **get_latest_raw_statement_value(
                    cashflow,
                    "Capital Expenditure",
                ),
                "unit": "USD",
                "taxonomy": (
                    "provider_capital_expenditure"
                ),
                "definition": (
                    "Yahoo Finance Capital Expenditure row. "
                    "May differ from SEC property-and-"
                    "equipment purchases."
                ),
            },
            "free_cash_flow": {
                **get_latest_raw_statement_value(
                    cashflow,
                    "Free Cash Flow",
                ),
                "unit": "USD",
                "taxonomy": "provider_free_cash_flow",
                "definition": (
                    "Yahoo Finance provider-defined free "
                    "cash flow."
                ),
            },
        }

        return {
            "currency": "USD",
            "provider": self.name,
            "period": (
                "Latest available annual periods via "
                "Yahoo Finance provider"
            ),
            "raw_metrics": raw_metrics,
            "income_statement": [
                ["Metric"] + periods,
                ["Revenue"] + _get_statement_row(income, "Total Revenue"),
                ["R&D Expense"] + _get_statement_row(income, "Research And Development"),
                ["Operating Income"] + _get_statement_row(income, "Operating Income"),
                ["Net Income"] + _get_statement_row(income, "Net Income"),
            ],
            "balance_sheet": [
                ["Metric", "Latest"],
                ["Cash & Equivalents", _get_statement_row(balance, "Cash And Cash Equivalents", 1)[0]],
                ["Total Debt", _get_statement_row(balance, "Total Debt", 1)[0]],
                ["Shareholders' Equity", _get_statement_row(balance, "Stockholders Equity", 1)[0]],
            ],
            "cash_flow": [
                ["Metric", "Latest"],
                ["Operating Cash Flow", _get_statement_row(cashflow, "Operating Cash Flow", 1)[0]],
                ["Capital Expenditures", _get_statement_row(cashflow, "Capital Expenditure", 1)[0]],
                ["Free Cash Flow", _get_statement_row(cashflow, "Free Cash Flow", 1)[0]],
            ],
            "financial_commentary": [
                f"Financial statements pulled using Yahoo Finance provider for {ticker}.",
                "Review revenue growth, operating margins, cash generation, leverage, and capital intensity together.",
            ],
        }
