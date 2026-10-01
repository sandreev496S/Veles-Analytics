from __future__ import annotations

from dataclasses import replace

from services.valuation.dcf_engine import calculate_dcf
from services.valuation.models import DCFAssumptions, DCFResult


def build_standard_scenarios(
    base: DCFAssumptions,
) -> dict[str, DCFAssumptions]:
    bull_growth = [
        growth + 0.05
        for growth in base.revenue_growth_rates
    ]

    bear_growth = [
        max(growth - 0.05, -0.50)
        for growth in base.revenue_growth_rates
    ]

    bull_margins = [
        margin + 0.05
        for margin in base.ebit_margins
    ]

    bear_margins = [
        margin - 0.05
        for margin in base.ebit_margins
    ]

    return {
        "bull": replace(
            base,
            scenario_name="Bull",
            revenue_growth_rates=bull_growth,
            ebit_margins=bull_margins,
            terminal_growth_rate=min(
                base.terminal_growth_rate + 0.005,
                0.04,
            ),
            equity_risk_premium=max(
                base.equity_risk_premium - 0.005,
                0.01,
            ),
        ),
        "base": replace(
            base,
            scenario_name="Base",
        ),
        "bear": replace(
            base,
            scenario_name="Bear",
            revenue_growth_rates=bear_growth,
            ebit_margins=bear_margins,
            terminal_growth_rate=max(
                base.terminal_growth_rate - 0.005,
                0.0,
            ),
            equity_risk_premium=(
                base.equity_risk_premium + 0.01
            ),
        ),
    }


def calculate_standard_scenarios(
    base: DCFAssumptions,
) -> dict[str, DCFResult]:
    return {
        name: calculate_dcf(assumptions)
        for name, assumptions in build_standard_scenarios(base).items()
    }
