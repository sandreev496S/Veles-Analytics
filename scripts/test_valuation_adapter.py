import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from services.orchestrator.research_orchestrator import (
    build_research_dataset,
)
from services.valuation import (
    CapitalMarketAssumptions,
    biotech_platform_profile,
    run_dcf_from_research,
)


def main() -> None:
    research = build_research_dataset(
        "RXRX",
        use_cache=True,
        selected_capabilities=[
            "company",
            "financials",
            "market",
            "filings",
            "company_facts",
        ],
    )

    result = run_dcf_from_research(
        research=research,
        forecast_profile=biotech_platform_profile(),
        capital_market_assumptions=CapitalMarketAssumptions(
            risk_free_rate=0.04,
            equity_risk_premium=0.055,
            cost_of_debt=0.07,
            debt_weight=0.05,
            equity_weight=0.95,
            source="Illustrative analyst assumptions",
            note=(
                "For engine testing only. "
                "Not a final RXRX valuation."
            ),
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

    snapshot = result["snapshot"]
    base_result = result["base_result"]

    print("Ticker:", snapshot["ticker"])
    print("Base year:", snapshot["base_year"])
    print(
        "Base revenue:",
        snapshot["base_revenue"]["value"],
    )
    print(
        "Cash:",
        snapshot["cash"]["value"],
    )
    print(
        "Debt:",
        snapshot["debt"]["value"],
    )
    print(
        "Shares:",
        snapshot["diluted_shares_outstanding"]["value"],
    )
    print(
        "Shares status:",
        snapshot["diluted_shares_outstanding"]["status"],
    )

    print(
        "DCF value/share:",
        f"${base_result['implied_value_per_share']:,.2f}",
    )

    print(
        "Warnings:",
        result["assumption_build"]["warnings"],
    )


if __name__ == "__main__":
    main()
