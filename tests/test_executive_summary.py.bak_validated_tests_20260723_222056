from services.reports.analyst_summary import (
    build_executive_summary,
)


def _build_summary():
    return build_executive_summary(
        company_name="Recursion Pharmaceuticals",
        ticker="RXRX",
        exchange="NASDAQ",
        industry="AI-Enabled Drug Discovery",
        company_description=(
            "Recursion uses machine learning and automated "
            "experimentation to support drug discovery. "
            "Its platform generates and analyzes large-scale "
            "biological datasets."
        ),
        income_statement=[
            ["Metric", "2025", "2024"],
            ["Revenue", "$58M", "$46M"],
            ["R&D Expense", "$310M", "$275M"],
            ["Net Income", "-$420M", "-$350M"],
        ],
        balance_sheet=[
            ["Metric", "2025", "2024"],
            ["Cash & Equivalents", "$518M", "$600M"],
            ["Total Debt", "$120M", "$130M"],
        ],
        cash_flow=[
            ["Metric", "2025", "2024"],
            ["Free Cash Flow", "-$360M", "-$300M"],
        ],
        estimated_runway="1.4 years",
        latest_filing=(
            "10-K — Annual report (2026-02-28)"
        ),
    )


def test_executive_summary_has_institutional_structure():
    summary = _build_summary()

    assert summary["title"] == "Executive Summary"
    assert summary["company"] == (
        "Recursion Pharmaceuticals (NASDAQ: RXRX)"
    )
    assert summary["industry"] == (
        "AI-Enabled Drug Discovery"
    )
    assert summary["business_model"]
    assert len(
        summary["investment_highlights"]
    ) >= 3
    assert len(summary["key_risks"]) >= 3
    assert len(summary["key_catalysts"]) >= 3


def test_executive_summary_preserves_renderer_compatibility():
    summary = _build_summary()

    assert summary["overview"]
    assert summary["financial_analysis"]
    assert summary["bull_case"] == (
        summary["investment_highlights"]
    )
    assert summary["bear_case"] == (
        summary["key_risks"]
    )


def test_executive_summary_contains_financial_snapshot():
    summary = _build_summary()
    snapshot = summary["financial_snapshot"]

    assert snapshot["Revenue"] == "$58M"
    assert snapshot["Cash"] == "$518M"
    assert snapshot["Debt"] == "$120M"
    assert snapshot["Estimated Runway"] == (
        "1.4 years"
    )


def test_executive_summary_identifies_cash_burn_risk():
    summary = _build_summary()

    assert any(
        "negative free cash flow" in risk.lower()
        for risk in summary["key_risks"]
    )
