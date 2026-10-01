from dataclasses import replace

import pytest

from services.valuation.biotech_driver_engine import (
    BiotechDriverInputError,
    calculate_biotech_driver_dcf,
    calculate_biotech_driver_scenarios,
)
from services.valuation.models import (
    BiotechDriverAssumptions,
)


def assumptions(years: int = 10):
    return BiotechDriverAssumptions(
        ticker="TEST",
        base_year=2025,
        base_collaboration_revenue=100_000_000,
        base_product_revenue=0,
        base_milestone_revenue=0,
        collaboration_growth_rates=[0.10] * years,
        product_revenue_forecast=[
            0,
            0,
            0,
            20_000_000,
            60_000_000,
            120_000_000,
            200_000_000,
            300_000_000,
            400_000_000,
            500_000_000,
            *(
                [
                    600_000_000,
                    700_000_000,
                    800_000_000,
                    900_000_000,
                    1_000_000_000,
                ]
                if years == 15
                else []
            ),
        ],
        milestone_revenue_forecast=[
            20_000_000
        ] * years,
        research_and_development_forecast=[
            max(
                450_000_000
                - 15_000_000 * index,
                250_000_000,
            )
            for index in range(years)
        ],
        selling_general_admin_forecast=[
            100_000_000 + 10_000_000 * index
            for index in range(years)
        ],
        other_operating_expense_forecast=[
            10_000_000
        ] * years,
        tax_rate=0.21,
        depreciation_amortization_pct_revenue=0.05,
        capex_pct_revenue=0.05,
        nwc_pct_revenue_change=0.04,
        risk_free_rate=0.04,
        equity_risk_premium=0.055,
        beta=1.0,
        cost_of_debt=0.07,
        debt_weight=0.05,
        equity_weight=0.95,
        terminal_growth_rate=0.025,
        cash=750_000_000,
        debt=80_000_000,
        diluted_shares_outstanding=500_000_000,
    )


@pytest.mark.parametrize("years", [10, 15])
def test_supported_forecast_horizons(years):
    result = calculate_biotech_driver_dcf(
        assumptions(years)
    )

    assert len(result.forecast) == years


def test_invalid_forecast_horizon_fails():
    with pytest.raises(BiotechDriverInputError):
        calculate_biotech_driver_dcf(
            assumptions(10).__class__(
                **{
                    **assumptions(10).__dict__,
                    "collaboration_growth_rates": [
                        0.10
                    ] * 5,
                }
            )
        )


def test_scenarios_are_monotonic():
    results = calculate_biotech_driver_scenarios(
        assumptions(10)
    )

    assert (
        results["bull"].implied_value_per_share
        >= results["base"].implied_value_per_share
        >= results["bear"].implied_value_per_share
    )


def test_driver_forecast_calculates_expenses():
    result = calculate_biotech_driver_dcf(
        assumptions(10)
    )

    first = result.forecast[0]

    assert first.research_and_development > 0
    assert first.selling_general_admin > 0
    assert first.total_operating_expense > 0


def test_high_terminal_margin_generates_warning():
    result = calculate_biotech_driver_dcf(
        assumptions(15)
    )

    if result.forecast[-1].ebit_margin > 0.40:
        assert any(
            "terminal-year ebit margin exceeds 40%"
            in warning.lower()
            for warning in result.warnings
        )
