from __future__ import annotations

import re
from typing import Any

from services.valuation.models import (
    ValuationDataSnapshot,
    ValuationInput,
)


MISSING_VALUES = {
    None,
    "",
    "N/A",
    "NA",
    "None",
    "Unknown",
    "-",
}


def parse_numeric(value: Any) -> float | None:
    """
    Convert Veles-formatted values such as:
    $743.29M
    $1.13B
    18.35M
    -3.77
    into raw floats.
    """
    if value in MISSING_VALUES:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip()

    if text in MISSING_VALUES:
        return None

    text = (
        text.replace("$", "")
        .replace(",", "")
        .replace("%", "")
        .strip()
    )

    multiplier = 1.0

    suffixes = {
        "T": 1_000_000_000_000,
        "B": 1_000_000_000,
        "M": 1_000_000,
        "K": 1_000,
    }

    if text and text[-1].upper() in suffixes:
        multiplier = suffixes[text[-1].upper()]
        text = text[:-1]

    try:
        return float(text) * multiplier
    except (TypeError, ValueError):
        return None


def extract_year(value: Any) -> int | None:
    if value is None:
        return None

    match = re.search(r"(19|20)\d{2}", str(value))

    if not match:
        return None

    return int(match.group(0))


def table_to_metric_map(
    table: list[list[Any]],
) -> dict[str, list[Any]]:
    """
    Convert a statement table into:
    {
        "Revenue": ["$74.26M", "$58.49M", "$43.88M"],
        ...
    }
    """
    result: dict[str, list[Any]] = {}

    if not table or len(table) < 2:
        return result

    for row in table[1:]:
        if not row:
            continue

        metric = str(row[0]).strip()
        result[metric] = list(row[1:])

    return result


def latest_statement_value(
    table: list[list[Any]],
    metric_names: list[str],
) -> tuple[float | None, str]:
    metric_map = table_to_metric_map(table)

    for metric_name in metric_names:
        values = metric_map.get(metric_name)

        if not values:
            continue

        parsed = parse_numeric(values[0])

        if parsed is not None:
            return parsed, metric_name

    return None, ""


def market_metric_map(
    market_snapshot: list[list[Any]],
) -> dict[str, Any]:
    result: dict[str, Any] = {}

    if not market_snapshot:
        return result

    for row in market_snapshot[1:]:
        if len(row) < 2:
            continue

        result[str(row[0]).strip()] = row[1]

    return result


def build_input(
    *,
    name: str,
    value: float | None,
    unit: str,
    source: str,
    source_key: str,
    note: str = "",
) -> ValuationInput:
    return ValuationInput(
        name=name,
        value=value,
        unit=unit,
        source=source,
        source_key=source_key,
        status="observed" if value is not None else "missing",
        note=note,
    )


def infer_diluted_shares(
    market_cap: float | None,
    share_price: float | None,
) -> tuple[float | None, str]:
    if (
        market_cap is None
        or share_price is None
        or share_price <= 0
    ):
        return None, ""

    return (
        market_cap / share_price,
        "Derived as market capitalization divided by share price",
    )


def adapt_research_dataset(
    research: dict[str, Any],
) -> ValuationDataSnapshot:
    ticker = str(research.get("ticker", "UNKNOWN")).upper()

    financials = research.get("financials", {})
    market = research.get("market", {})

    income_statement = financials.get(
        "income_statement",
        [],
    )
    balance_sheet = financials.get(
        "balance_sheet",
        [],
    )

    headers = (
        income_statement[0][1:]
        if income_statement and len(income_statement[0]) > 1
        else []
    )

    base_year = (
        extract_year(headers[0])
        if headers
        else None
    )

    revenue, revenue_key = latest_statement_value(
        income_statement,
        [
            "Revenue",
            "Total Revenue",
            "Revenue From Contract With Customer",
        ],
    )

    cash, cash_key = latest_statement_value(
        balance_sheet,
        [
            "Cash & Equivalents",
            "Cash And Cash Equivalents",
            "Cash Cash Equivalents And Short Term Investments",
        ],
    )

    debt, debt_key = latest_statement_value(
        balance_sheet,
        [
            "Total Debt",
            "Long Term Debt",
            "Debt Current",
        ],
    )

    market_snapshot = market.get(
        "tables",
        {},
    ).get(
        "market_snapshot",
        [],
    )

    market_metrics = market_metric_map(market_snapshot)

    share_price = parse_numeric(
        market_metrics.get("Share Price")
    )
    market_cap = parse_numeric(
        market_metrics.get("Market Cap")
    )
    enterprise_value = parse_numeric(
        market_metrics.get("Enterprise Value")
    )
    beta = parse_numeric(
        market_metrics.get("Beta")
    )

    inferred_shares, shares_note = infer_diluted_shares(
        market_cap,
        share_price,
    )

    warnings: list[str] = []

    if revenue is None:
        warnings.append(
            "Base revenue could not be extracted from the normalized income statement."
        )

    if cash is None:
        warnings.append(
            "Cash could not be extracted from the normalized balance sheet."
        )

    if debt is None:
        warnings.append(
            "Debt could not be extracted from the normalized balance sheet."
        )

    if beta is None:
        warnings.append(
            "Beta was not available from normalized market data."
        )

    if inferred_shares is None:
        warnings.append(
            "Diluted shares could not be inferred from market cap and share price."
        )

    if base_year is None:
        warnings.append(
            "The latest financial statement year could not be determined."
        )

    return ValuationDataSnapshot(
        ticker=ticker,
        base_year=base_year,
        base_revenue=build_input(
            name="Base Revenue",
            value=revenue,
            unit="USD",
            source="Normalized income statement",
            source_key=revenue_key or "Revenue",
        ),
        cash=build_input(
            name="Cash and Equivalents",
            value=cash,
            unit="USD",
            source="Normalized balance sheet",
            source_key=cash_key or "Cash & Equivalents",
        ),
        debt=build_input(
            name="Total Debt",
            value=debt,
            unit="USD",
            source="Normalized balance sheet",
            source_key=debt_key or "Total Debt",
        ),
        beta=build_input(
            name="Beta",
            value=beta,
            unit="multiple",
            source="Normalized market data",
            source_key="Beta",
        ),
        market_cap=build_input(
            name="Market Capitalization",
            value=market_cap,
            unit="USD",
            source="Normalized market data",
            source_key="Market Cap",
        ),
        enterprise_value=build_input(
            name="Enterprise Value",
            value=enterprise_value,
            unit="USD",
            source="Normalized market data",
            source_key="Enterprise Value",
        ),
        diluted_shares_outstanding=ValuationInput(
            name="Diluted Shares Outstanding",
            value=inferred_shares,
            unit="shares",
            source="Derived from normalized market data",
            source_key="Market Cap / Share Price",
            status=(
                "derived"
                if inferred_shares is not None
                else "missing"
            ),
            note=shares_note,
        ),
        share_price=build_input(
            name="Share Price",
            value=share_price,
            unit="USD/share",
            source="Normalized market data",
            source_key="Share Price",
        ),
        metadata={
            "research_generated_at": research.get(
                "metadata",
                {},
            ).get(
                "generated_at"
            ),
            "adapter": "Veles Valuation Data Adapter v1",
        },
        warnings=warnings,
    )
