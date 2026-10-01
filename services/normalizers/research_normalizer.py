from typing import Any, Dict


def _safe(value: Any, default: str = "N/A") -> Any:
    if value is None or value == "":
        return default
    return value


def normalize_company(raw_company: Dict[str, Any], ticker: str) -> Dict[str, Any]:
    return {
        "company_name": _safe(raw_company.get("company_name"), ticker.upper()),
        "ticker": _safe(raw_company.get("ticker"), ticker.upper()),
        "exchange": _safe(raw_company.get("exchange")),
        "sector": _safe(raw_company.get("sector")),
        "industry": _safe(raw_company.get("industry")),
        "website": _safe(raw_company.get("website")),
        "headquarters": _safe(raw_company.get("headquarters")),
        "description": _safe(raw_company.get("description")),
        "business_model": _safe(raw_company.get("business_model")),
        "report_view": _safe(raw_company.get("report_view")),
        "stage": _safe(raw_company.get("stage")),
        "ceo": _safe(raw_company.get("ceo")),
        "founded": _safe(raw_company.get("founded")),
    }


def normalize_market(raw_market: Dict[str, Any]) -> Dict[str, Any]:
    market_snapshot = raw_market.get("market_snapshot", [])
    valuation_multiples = raw_market.get("valuation_multiples", [])

    metrics = {}
    for row in market_snapshot[1:]:
        if len(row) >= 2:
            metrics[row[0]] = row[1]

    for row in valuation_multiples[1:]:
        if len(row) >= 2:
            metrics[row[0]] = row[1]

    return {
        "currency": _safe(raw_market.get("currency"), "USD"),
        "as_of": _safe(raw_market.get("as_of")),
        "metrics": metrics,
        "raw_metrics": raw_market.get(
            "raw_metrics",
            {},
        ),
        "provider": _safe(
            raw_market.get("provider"),
            "unknown",
        ),
        "tables": {
            "market_snapshot": market_snapshot,
            "valuation_multiples": valuation_multiples,
        },
        "commentary": raw_market.get("market_commentary", []),
    }


def normalize_financials(raw_financials: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "currency": _safe(raw_financials.get("currency"), "USD"),
        "period": _safe(raw_financials.get("period")),
        "provider": _safe(
            raw_financials.get("provider"),
            "unknown",
        ),
        "raw_metrics": raw_financials.get(
            "raw_metrics",
            {},
        ),
        "income_statement": raw_financials.get("income_statement", []),
        "balance_sheet": raw_financials.get("balance_sheet", []),
        "cash_flow": raw_financials.get("cash_flow", []),
        "commentary": raw_financials.get("financial_commentary", []),
    }


def normalize_sec(raw_filings: Dict[str, Any], raw_company_facts: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "filings": {
            "status": raw_filings.get("status", "N/A"),
            "source": raw_filings.get("source", "N/A"),
            "cik": raw_filings.get("cik", "N/A"),
            "company_name": raw_filings.get("company_name", "N/A"),
            "sic": raw_filings.get("sic", "N/A"),
            "sic_description": raw_filings.get("sic_description", "N/A"),
            "recent": raw_filings.get("filings", []),
        },
        "company_facts": {
            "status": raw_company_facts.get("status", "N/A"),
            "source": raw_company_facts.get("source", "N/A"),
            "entity_name": raw_company_facts.get("entity_name", "N/A"),
            "facts": raw_company_facts.get("facts", {}),
        },
    }


def normalize_research_dataset(raw_dataset: Dict[str, Any]) -> Dict[str, Any]:
    ticker = raw_dataset.get("ticker", "N/A")

    return {
        "ticker": ticker,
        "company": normalize_company(raw_dataset.get("company", {}), ticker),
        "market": normalize_market(raw_dataset.get("market", {})),
        "financials": normalize_financials(raw_dataset.get("financials", {})),
        "sec": normalize_sec(
            raw_dataset.get("filings", {}),
            raw_dataset.get("company_facts", {}),
        ),
        "raw": raw_dataset,
        "metadata": {
            **raw_dataset.get("metadata", {}),
            "normalized": True,
            "normalizer": "Veles Research Normalizer v1",
        },
    }
