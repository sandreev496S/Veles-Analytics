from __future__ import annotations

from typing import Any

from services.valuation.assumption_builder import (
    AssumptionBuildResult,
    CapitalMarketAssumptions,
    ForecastProfile,
    build_dcf_assumptions,
)
from services.valuation.data_adapter import (
    adapt_research_dataset,
)
from services.valuation.dcf_engine import (
    calculate_dcf,
    calculate_sensitivity,
)
from services.valuation.models import (
    DCFResult,
    SensitivityResult,
    ValuationDataSnapshot,
)
from services.valuation.scenarios import (
    calculate_standard_scenarios,
)


def build_valuation_snapshot(
    research: dict[str, Any],
) -> ValuationDataSnapshot:
    return adapt_research_dataset(research)


def run_dcf_from_research(
    research: dict[str, Any],
    forecast_profile: ForecastProfile,
    capital_market_assumptions: CapitalMarketAssumptions,
    *,
    scenario_name: str = "Base",
    sensitivity_wacc_values: list[float] | None = None,
    sensitivity_terminal_growth_values: list[float] | None = None,
) -> dict[str, Any]:
    snapshot = build_valuation_snapshot(research)

    build_result = build_dcf_assumptions(
        snapshot=snapshot,
        forecast_profile=forecast_profile,
        capital_market_assumptions=capital_market_assumptions,
        scenario_name=scenario_name,
    )

    base_result = calculate_dcf(
        build_result.assumptions
    )

    scenarios = calculate_standard_scenarios(
        build_result.assumptions
    )

    sensitivity: SensitivityResult | None = None

    if (
        sensitivity_wacc_values
        and sensitivity_terminal_growth_values
    ):
        sensitivity = calculate_sensitivity(
            build_result.assumptions,
            wacc_values=sensitivity_wacc_values,
            terminal_growth_values=(
                sensitivity_terminal_growth_values
            ),
        )

    return {
        "snapshot": snapshot.to_dict(),
        "assumption_build": build_result.to_dict(),
        "base_result": base_result.to_dict(),
        "scenarios": {
            name: result.to_dict()
            for name, result in scenarios.items()
        },
        "sensitivity": (
            sensitivity.to_dict()
            if sensitivity
            else None
        ),
    }
