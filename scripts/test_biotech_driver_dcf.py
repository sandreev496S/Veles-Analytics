from __future__ import annotations

from services.orchestrator.research_orchestrator import (
    build_research_dataset,
)
from services.valuation import (
    run_biotech_driver_valuation,
    save_valuation,
)
from services.valuation.integration_validation import (
    validate_complete_dcf_payload,
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

    for horizon in [10, 15]:
        print(f"Running {horizon}-year driver DCF")

        payload = run_biotech_driver_valuation(
            research,
            forecast_years=horizon,
        )

        validate_complete_dcf_payload(payload)

        scenarios = payload["scenarios"]

        bull = scenarios["bull"][
            "implied_value_per_share"
        ]
        base = scenarios["base"][
            "implied_value_per_share"
        ]
        bear = scenarios["bear"][
            "implied_value_per_share"
        ]

        assert bull >= base >= bear

        print(
            "Scenario values:",
            f"Bull={bull:.2f}",
            f"Base={base:.2f}",
            f"Bear={bear:.2f}",
        )

        path = save_valuation(
            ticker="RXRX",
            payload=payload,
            name=(
                f"RXRX Illustrative "
                f"{horizon}-Year Driver DCF"
            ),
        )

        print("Saved:", path)


if __name__ == "__main__":
    main()
