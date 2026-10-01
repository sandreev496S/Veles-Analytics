from __future__ import annotations

from pathlib import Path

from services.orchestrator.research_orchestrator import (
    build_research_dataset,
)
from services.pdf_report_exporter import (
    export_equity_report_pdf_v2,
)
from services.reports.equity_report_assembler import (
    assemble_equity_report,
)
from services.valuation import (
    CapitalMarketAssumptions,
    biotech_platform_profile,
    load_latest_valuation,
    run_dcf_from_research,
    save_valuation,
)
from services.valuation.integration_validation import (
    validate_complete_dcf_payload,
)


TICKER = "RXRX"


def main() -> None:
    print("1. Building normalized research dataset")

    research = build_research_dataset(
        TICKER,
        use_cache=True,
        selected_capabilities=[
            "company",
            "financials",
            "market",
            "filings",
            "company_facts",
        ],
    )

    print("2. Running DCF")

    payload = run_dcf_from_research(
        research=research,
        forecast_profile=biotech_platform_profile(),
        capital_market_assumptions=CapitalMarketAssumptions(
            risk_free_rate=0.04,
            equity_risk_premium=0.055,
            cost_of_debt=0.07,
            debt_weight=0.05,
            equity_weight=0.95,
            source="Illustrative analyst assumptions",
            note="Integration test only. Not investment advice.",
        ),
        sensitivity_wacc_values=[
            0.09,
            0.10,
            0.11,
            0.12,
            0.13,
        ],
        sensitivity_terminal_growth_values=[
            0.01,
            0.015,
            0.02,
            0.025,
            0.03,
        ],
    )

    validate_complete_dcf_payload(payload)

    print("3. Saving DCF")

    saved_path = save_valuation(
        ticker=TICKER,
        payload=payload,
        name="RXRX Integration Test DCF",
    )

    print("Saved:", saved_path)

    print("4. Reloading saved DCF")

    latest = load_latest_valuation(TICKER)

    if latest is None:
        raise RuntimeError("Saved valuation could not be reloaded.")

    validate_complete_dcf_payload(latest["payload"])

    print("5. Assembling equity report")

    report = assemble_equity_report(TICKER)

    status = report.valuation.get("status")
    print("Valuation status:", status)

    if status != "available":
        raise RuntimeError(
            "Valuation did not reach ReportDocument: "
            + str(report.valuation)
        )

    print("6. Exporting PDF")

    output_path = Path(
        "reports/generated/rxrx_dcf_integration_smoke_test.pdf"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output = export_equity_report_pdf_v2(
        report,
        str(output_path),
    )

    if not output_path.exists():
        raise RuntimeError("DCF report PDF was not created.")

    print("SUCCESS:", output)


if __name__ == "__main__":
    main()
