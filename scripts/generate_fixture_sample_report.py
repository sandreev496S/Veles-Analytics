from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt

from services.data_quality.validated_metric import (
    MetricConfidence,
    MetricProvenance,
    MetricSourceType,
    MetricValidationStatus,
    ValidatedMetric,
)
from services.pdf_report_exporter import export_equity_report_pdf_v2
from services.reports.financial_render_models import build_financial_render_model
from services.reports.reconciliation import validate_report_for_delivery


def _metric(name: str, value: float, period: date, *, unit: str = "USD", source: str = "SEC fixture") -> ValidatedMetric:
    return ValidatedMetric(
        name=name,
        display_name=name.replace("_", " ").title(),
        value=value,
        unit=unit,
        confidence=MetricConfidence.HIGH,
        validation_status=MetricValidationStatus.VERIFIED,
        provenance=MetricProvenance(
            source_type=MetricSourceType.SEC,
            source_name=source,
            period_end=period,
        ),
        period_end=period,
    )


def _save_line_chart(path: Path, years: list[str], series: list[tuple[str, list[float]]], title: str, ylabel: str) -> None:
    fig, ax = plt.subplots(figsize=(8.4, 3.2))
    for label, values in series:
        ax.plot(years, values, marker="o", label=label)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.25)
    if len(series) > 1:
        ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _save_bar_chart(path: Path, labels: list[str], values: list[float], title: str, ylabel: str) -> None:
    fig, ax = plt.subplots(figsize=(8.4, 3.2))
    ax.bar(labels, values)
    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.grid(True, axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def build_report(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    chart_dir = output_dir / "charts"
    chart_dir.mkdir(exist_ok=True)

    years = ["2023", "2024", "2025"]
    _save_line_chart(chart_dir / "revenue.png", years, [("Revenue", [42, 57, 74])], "Revenue Trend", "USD millions")
    _save_line_chart(chart_dir / "rd.png", years, [("R&D", [118, 142, 168])], "R&D Expense Trend", "USD millions")
    _save_line_chart(chart_dir / "loss.png", years, [("Operating loss", [-155, -176, -201]), ("Net loss", [-148, -169, -195])], "Operating and Net Loss Trend", "USD millions")
    _save_bar_chart(chart_dir / "cash_debt.png", ["Cash", "Debt"], [500, 100], "Cash Versus Debt", "USD millions")
    _save_bar_chart(chart_dir / "market_ev.png", ["Market cap", "Enterprise value"], [2000, 1600], "Market Capitalization Versus Enterprise Value", "USD millions")

    balance_period = date(2025, 12, 31)
    market_period = date(2026, 1, 15)
    registry = {
        "share_price": _metric("share_price", 20.0, market_period),
        "market_cap": _metric("market_cap", 2_000_000_000, market_period),
        "cash": _metric("cash", 500_000_000, balance_period),
        "financial_debt": _metric("financial_debt", 100_000_000, balance_period),
        "reconciled_enterprise_value": _metric("reconciled_enterprise_value", 1_600_000_000, market_period),
    }
    model = build_financial_render_model(registry)

    report = {
        "company_name": "Test Therapeutics",
        "ticker": "TEST",
        "industry": "Clinical-Stage Biotechnology",
        "date": "January 15, 2026",
        "metadata": {
            "market_data_as_of": "2026-01-15",
            "latest_sec_filing_date": "2025-12-31",
            "generated_at": "2026-01-15 12:00 UTC",
        },
        "report_profile": {
            "name": "professional",
            "include_ai_commentary": True,
            "include_valuation": True,
            "include_dcf": True,
            "include_comps": True,
            "include_scenarios": True,
            "include_sensitivity": True,
            "include_price_target": True,
            "include_rating": True,
            "include_methodology": True,
            "include_appendix": True,
        },
        "financial_render_model": model.to_dict(),
        "executive_summary": {
            "company": "Test Therapeutics (NASDAQ: TEST)",
            "industry": "Clinical-Stage Biotechnology",
            "business_model": "Test Therapeutics develops precision medicines and funds development through cash reserves, collaborations, and capital markets.",
            "investment_highlights": [
                "A $500.0M cash balance provides meaningful funding capacity.",
                "Revenue increased from $42M in 2023 to $74M in 2025.",
                "The illustrative DCF implies $24.00 per share versus a $20.00 market price.",
            ],
            "key_risks": [
                "Operating losses and cash burn remain elevated.",
                "Clinical outcomes and development timelines are uncertain.",
                "Future financing could dilute shareholders.",
            ],
            "key_catalysts": [
                "Lead-program clinical data.",
                "New collaboration agreements.",
                "Quarterly financial updates.",
            ],
            "financial_snapshot": {
                "Revenue": "$74M",
                "Cash": "$500.0M",
                "Debt": "$100.0M",
                "Market Cap": "$2.00B",
                "Enterprise Value": "$1.60B",
                "Share Price": "$20.00",
            },
            "metrics": {"cash": "$500.0M", "market_cap": "$2.00B", "share_price": "$20.00"},
        },
        "dashboard_metrics": [
            {"label": "Share Price", "value": "$20.00", "note": "As of Jan. 15, 2026"},
            {"label": "Market Cap", "value": "$2.00B", "note": "Current equity value"},
            {"label": "Cash", "value": "$500.0M", "note": "FY2025 period end"},
            {"label": "Total Debt", "value": "$100.0M", "note": "FY2025 period end"},
            {"label": "Enterprise Value", "value": "$1.60B", "note": "Reconciled"},
            {"label": "FY2025 Revenue", "value": "$74.0M", "note": "+29.8% YoY"},
            {"label": "Net Cash", "value": "$400.0M", "note": "Cash less debt"},
            {"label": "DCF Value / Share", "value": "$24.00", "note": "Illustrative base case"},
        ],
        "dashboard_business": {"Stage": "Clinical", "Primary focus": "Precision oncology", "Revenue model": "Collaborations"},
        "dashboard_investment": {"Rating": "Speculative Buy", "Price target": "$24.00", "Upside": "20.0%"},
        "snapshot": {"Headquarters": "Cambridge, Massachusetts", "Exchange": "NASDAQ", "Employees": "420", "Fiscal year end": "December 31", "Currency": "USD"},
        "charts": {
            "revenue_trend": str(chart_dir / "revenue.png"),
            "rd_expense_trend": str(chart_dir / "rd.png"),
            "operating_net_loss_trend": str(chart_dir / "loss.png"),
            "cash_vs_debt": str(chart_dir / "cash_debt.png"),
            "market_cap_vs_ev": str(chart_dir / "market_ev.png"),
            "capital_structure": {"metrics": {"cash": 500_000_000, "financial_debt": 100_000_000}},
        },
        "financial_table": [["Metric", "Value"], ["FY2025 Revenue", "$74.0M"], ["Cash", "$500.0M"], ["Debt", "$100.0M"], ["Net Cash", "$400.0M"]],
        "income_statement": [["USD millions", "2023", "2024", "2025"], ["Revenue", "42", "57", "74"], ["R&D expense", "(118)", "(142)", "(168)"], ["Operating loss", "(155)", "(176)", "(201)"], ["Net loss", "(148)", "(169)", "(195)"]],
        "balance_sheet": [["Metric", "FY2025"], ["Cash and equivalents", "$500.0M"], ["Financial debt", "$100.0M"], ["Net cash", "$400.0M"]],
        "cash_flow": [["Metric", "FY2025"], ["Operating cash flow", "($162.0M)"], ["Capital expenditures", "($18.0M)"], ["Free cash flow", "($180.0M)"]],
        "sec_filings_table": [["Form", "Filed", "Period", "Description"], ["10-K", "2026-02-20", "2025-12-31", "Annual report"], ["8-K", "2026-01-10", "N/A", "Clinical-program update"]],
        "sec_commentary": ["The annual report is the primary source for FY2025 financial statements.", "The January 8-K disclosed a clinical-program update without changing the financial baseline."],
        "market_snapshot": [["Metric", "Value"], ["Share Price", "$20.00"], ["Market Capitalization", "$2.00B"], ["Enterprise Value", "$1.60B"], ["52-Week Range", "$12.40 - $23.80"]],
        "valuation_multiples": [["Metric", "Value"], ["EV / FY2025 Revenue", "21.6x"], ["Market Cap / Cash", "4.0x"]],
        "market_commentary": ["Enterprise value is below market capitalization because the company holds $400.0M of net cash.", "The revenue multiple remains high and depends on future clinical and commercial execution."],
        "analyst_commentary": {
            "executive_summary": {"text": "The company combines improving collaboration revenue with a strong net-cash position, but sustained operating losses preserve a high-risk profile.", "evidence_ids": ["FIN-REV-2025", "BS-CASH-2025", "VAL-BASE"], "confidence": "high"},
            "revenue_analysis": {"text": "Revenue rose in each observed year and reached $74M in FY2025.", "evidence_ids": ["FIN-REV-2023-2025"], "confidence": "high"},
            "liquidity_analysis": {"text": "Cash of $500M exceeds financial debt of $100M, leaving $400M of net cash.", "evidence_ids": ["BS-CASH-2025", "BS-DEBT-2025"], "confidence": "high"},
            "profitability_analysis": {"text": "Operating and net losses widened as research investment increased.", "evidence_ids": ["IS-LOSS-2023-2025"], "confidence": "high"},
            "market_valuation_analysis": {"text": "The base-case DCF indicates $24.00 per share, or 20% upside to the current $20.00 price.", "evidence_ids": ["VAL-BASE", "MKT-PRICE-2026-01-15"], "confidence": "medium"},
            "risk_assessment": {"text": "The principal risks are clinical failure, cash burn, and dilution.", "evidence_ids": ["RISK-CLINICAL", "CF-FCF-2025"], "confidence": "medium"},
            "catalyst_assessment": {"text": "Clinical readouts and collaboration announcements are the most important potential catalysts.", "evidence_ids": ["CAT-PIPELINE"], "confidence": "medium"},
            "limitations": [],
        },
        "sections": [
            {"heading": "Company Overview", "body": "Test Therapeutics is a fictional clinical-stage biotechnology company used to validate the Veles report pipeline."},
            {"heading": "Business Model", "body": "The company is modeled as receiving collaboration revenue while investing heavily in internally developed precision-medicine programs."},
            {"heading": "Technology & Platform Analysis", "body": "The demonstration assumes a differentiated discovery platform. No real-world scientific claim is made."},
            {"heading": "Valuation Discussion", "body": "The illustrative DCF is designed to test consistency across the executive summary, dashboard, valuation section, and report reconciliation gate."},
            {"heading": "Disclaimer", "body": "This sample is fictional and for software quality assurance only. It is not investment advice."},
        ],
        "valuation": {
            "status": "available",
            "method": "Enterprise DCF",
            "name": "Fixture Base Case",
            "forecast_years": 5,
            "model_status": "illustrative",
            "model_note": "Deterministic QA model using fixed fixture assumptions.",
            "assumption_source": "Veles test fixture",
            "metrics": {"market_cap": 2_000_000_000, "share_price": 20.0, "reconciled_enterprise_value": 1_600_000_000},
            "summary": {"implied_value_per_share": "$24.00", "current_share_price": "$20.00", "implied_upside": "20.0%", "wacc": "11.0%", "enterprise_value": "$2.00B", "equity_value": "$2.40B"},
            "scenario_table": [["Scenario", "Value / Share", "Upside / Downside", "Rating"], ["Bull", "$31.00", "55.0%", "Buy"], ["Base", "$24.00", "20.0%", "Speculative Buy"], ["Bear", "$12.00", "(40.0%)", "Sell"]],
            "forecast_table": [["Year", "Revenue", "EBIT margin", "Tax", "NOPAT", "D&A / Capex", "UFCF"], ["2026E", "$92M", "(180%)", "$0M", "($166M)", "($12M)", "($178M)"], ["2027E", "$128M", "(120%)", "$0M", "($154M)", "($8M)", "($162M)"], ["2028E", "$185M", "(65%)", "$0M", "($120M)", "$2M", "($118M)"], ["2029E", "$275M", "(20%)", "$0M", "($55M)", "$8M", "($47M)"], ["2030E", "$410M", "15%", "$9M", "$53M", "$12M", "$65M"]],
            "sensitivity_table": [["WACC / g", "2.0%", "2.5%", "3.0%"], ["10.0%", "$23.10", "$24.70", "$26.60"], ["11.0%", "$22.50", "$24.00", "$25.70"], ["12.0%", "$21.90", "$23.30", "$24.80"]],
            "assumption_table": [["Assumption", "Value", "Source"], ["WACC", "11.0%", "Analyst fixture"], ["Terminal growth", "2.5%", "Analyst fixture"], ["Net cash", "$400.0M", "Validated FY2025 balance sheet"]],
            "limitations": ["Illustrative values only.", "No probability-adjusted clinical valuation is included."],
        },
    }

    validate_report_for_delivery(report, raise_on_error=True)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the deterministic Veles QA sample report.")
    parser.add_argument("--output-dir", default="reports/qa_sample")
    args = parser.parse_args()
    output_dir = Path(args.output_dir).resolve()
    report = build_report(output_dir)
    json_path = output_dir / "test_therapeutics_report.json"
    pdf_path = output_dir / "test_therapeutics_equity_research.pdf"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    export_equity_report_pdf_v2(report, pdf_path)
    print(pdf_path)


if __name__ == "__main__":
    main()
