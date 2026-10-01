from __future__ import annotations

from dataclasses import replace
from typing import Any

from services.valuation.biotech_driver_engine import (
    calculate_biotech_driver_dcf,
    calculate_biotech_driver_scenarios,
)
from services.valuation.biotech_driver_profiles import (
    build_biotech_driver_profile,
)
from services.valuation.data_adapter import (
    adapt_research_dataset,
)


def run_biotech_driver_valuation(
    research: dict[str, Any],
    *,
    forecast_years: int = 10,
    wacc_values: list[float] | None = None,
    terminal_growth_values: list[float] | None = None,
) -> dict[str, Any]:
    snapshot = adapt_research_dataset(research)

    assumptions = build_biotech_driver_profile(
        snapshot,
        forecast_years=forecast_years,
    )

    base_result = calculate_biotech_driver_dcf(
        assumptions
    )

    scenarios = calculate_biotech_driver_scenarios(
        assumptions
    )

    wacc_values = wacc_values or [
        0.09,
        0.10,
        0.11,
        0.12,
        0.13,
    ]
    terminal_growth_values = (
        terminal_growth_values
        or [0.01, 0.015, 0.02, 0.025, 0.03]
    )

    sensitivity_cells: list[dict[str, float]] = []

    for target_wacc in wacc_values:
        for terminal_growth in terminal_growth_values:
            after_tax_debt_cost = (
                assumptions.cost_of_debt
                * (1 - assumptions.tax_rate)
            )

            implied_cost_of_equity = (
                target_wacc
                - assumptions.debt_weight
                * after_tax_debt_cost
            ) / assumptions.equity_weight

            implied_erp = (
                implied_cost_of_equity
                - assumptions.risk_free_rate
            ) / assumptions.beta

            sensitivity_assumptions = replace(
                assumptions,
                equity_risk_premium=implied_erp,
                terminal_growth_rate=terminal_growth,
                scenario_name=(
                    f"WACC {target_wacc:.1%} / "
                    f"Terminal Growth {terminal_growth:.1%}"
                ),
            )

            result = calculate_biotech_driver_dcf(
                sensitivity_assumptions
            )

            sensitivity_cells.append({
                "wacc": target_wacc,
                "terminal_growth_rate": terminal_growth,
                "enterprise_value": result.enterprise_value,
                "equity_value": result.equity_value,
                "implied_value_per_share": (
                    result.implied_value_per_share
                ),
            })

    return {
        "model_type": "biotech_driver_dcf",
        "model_status": assumptions.model_status,
        "model_note": assumptions.model_note,
        "forecast_years": forecast_years,
        "snapshot": snapshot.to_dict(),
        "base_result": base_result.to_dict(),
        "scenarios": {
            name: result.to_dict()
            for name, result in scenarios.items()
        },
        "sensitivity": {
            "wacc_values": wacc_values,
            "terminal_growth_values": (
                terminal_growth_values
            ),
            "cells": sensitivity_cells,
        },
        "assumption_build": {
            "assumptions": (
                base_result.to_dict()["assumptions"]
            ),
            "warnings": base_result.warnings,
            "classification": (
                "Illustrative analyst scenario"
            ),
        },
    }
