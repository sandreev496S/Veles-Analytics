from __future__ import annotations

from typing import Any


def _table_records(
    prefix: str,
    table: list[list[Any]],
    source: str,
) -> list[dict[str, Any]]:
    if not table or len(table) < 2:
        return []

    headers = [str(item) for item in table[0]]
    records: list[dict[str, Any]] = []

    for row_index, row in enumerate(table[1:], start=1):
        if not row:
            continue

        values = {
            headers[index]: value
            for index, value in enumerate(row)
            if index < len(headers)
        }

        records.append({
            "evidence_id": f"{prefix}.{row_index}",
            "source": source,
            "data": values,
        })

    return records


def build_ai_evidence_packet(
    research: dict[str, Any],
) -> dict[str, Any]:
    company = research.get("company", {})
    financials = research.get("financials", {})
    market = research.get("market", {})
    sec = research.get("sec", {})

    evidence: list[dict[str, Any]] = []

    company_fields = {
        "company_name": company.get("company_name"),
        "ticker": company.get("ticker"),
        "exchange": company.get("exchange"),
        "sector": company.get("sector"),
        "industry": company.get("industry"),
        "headquarters": company.get("headquarters"),
        "description": company.get("description"),
        "business_model": company.get("business_model"),
    }

    for key, value in company_fields.items():
        if value not in {None, "", "N/A", "Unknown"}:
            evidence.append({
                "evidence_id": f"company.{key}",
                "source": "Normalized company provider data",
                "data": value,
            })

    evidence.extend(
        _table_records(
            "financials.income",
            financials.get("income_statement", []),
            "Normalized annual income statement",
        )
    )
    evidence.extend(
        _table_records(
            "financials.balance",
            financials.get("balance_sheet", []),
            "Normalized balance sheet",
        )
    )
    evidence.extend(
        _table_records(
            "financials.cashflow",
            financials.get("cash_flow", []),
            "Normalized cash-flow statement",
        )
    )

    evidence.extend(
        _table_records(
            "market.snapshot",
            market.get("tables", {}).get("market_snapshot", []),
            "Normalized live market data",
        )
    )
    evidence.extend(
        _table_records(
            "market.multiples",
            market.get("tables", {}).get("valuation_multiples", []),
            "Normalized valuation multiples",
        )
    )

    filings = sec.get("filings", {}).get("recent", [])

    for index, filing in enumerate(filings[:10], start=1):
        evidence.append({
            "evidence_id": f"sec.filing.{index}",
            "source": "SEC EDGAR submissions API",
            "data": {
                "form": filing.get("form"),
                "filing_date": filing.get("filing_date"),
                "report_date": filing.get("report_date"),
                "primary_document": filing.get("primary_document"),
            },
        })

    return {
        "ticker": research.get("ticker"),
        "generated_at": research.get("metadata", {}).get("generated_at"),
        "evidence": evidence,
    }
