import pytest

from services.valuation import (
    DCFAssumptions,
    ValuationInputError,
    calculate_dcf,
    calculate_sensitivity,
    calculate_standard_scenarios,
)


@pytest.fixture
def assumptions() -> DCFAssumptions:
    return DCFAssumptions(
        ticker="TEST",
        base_year=2025,
        base_revenue=100_000_000,
        revenue_growth_rates=[
            0.20,
            0.18,
            0.15,
            0.12,
            0.10,
        ],
        ebit_margins=[
            -0.30,
            -0.15,
            0.00,
            0.10,
            0.18,
        ],
        tax_rate=0.21,
        depreciation_amortization_pct_revenue=0.04,
        capex_pct_revenue=0.05,
        nwc_pct_revenue_change=0.08,
        risk_free_rate=0.04,
        equity_risk_premium=0.055,
        beta=1.20,
        cost_of_debt=0.07,
        debt_weight=0.10,
        equity_weight=0.90,
        terminal_growth_rate=0.025,
        cash=250_000_000,
        debt=50_000_000,
        diluted_shares_outstanding=100_000_000,
        scenario_name="Base",
    )


def test_dcf_returns_five_forecast_years(
    assumptions: DCFAssumptions,
):
    result = calculate_dcf(assumptions)

    assert len(result.forecast) == 5
    assert result.forecast[0].year == 2026
    assert result.forecast[-1].year == 2030


def test_revenue_compounds_correctly(
    assumptions: DCFAssumptions,
):
    result = calculate_dcf(assumptions)

    expected_first_year = 100_000_000 * 1.20

    assert result.forecast[0].revenue == pytest.approx(
        expected_first_year
    )


def test_equity_value_reconciles_from_enterprise_value(
    assumptions: DCFAssumptions,
):
    result = calculate_dcf(assumptions)

    expected_equity_value = (
        result.enterprise_value
        - assumptions.debt
        + assumptions.cash
    )

    assert result.equity_value == pytest.approx(
        expected_equity_value
    )


def test_value_per_share_is_calculated(
    assumptions: DCFAssumptions,
):
    result = calculate_dcf(assumptions)

    assert result.implied_value_per_share == pytest.approx(
        result.equity_value
        / assumptions.diluted_shares_outstanding
    )


def test_sensitivity_generates_requested_grid(
    assumptions: DCFAssumptions,
):
    result = calculate_sensitivity(
        assumptions,
        wacc_values=[0.09, 0.10, 0.11],
        terminal_growth_values=[0.02, 0.025, 0.03],
    )

    assert len(result.cells) == 9


def test_standard_scenarios_are_generated(
    assumptions: DCFAssumptions,
):
    scenarios = calculate_standard_scenarios(assumptions)

    assert set(scenarios) == {"bull", "base", "bear"}


def test_wacc_must_exceed_terminal_growth(
    assumptions: DCFAssumptions,
):
    invalid = DCFAssumptions(
        **{
            **assumptions.__dict__,
            "risk_free_rate": 0.01,
            "equity_risk_premium": 0.01,
            "beta": 1.0,
            "terminal_growth_rate": 0.04,
        }
    )

    with pytest.raises(ValuationInputError):
        calculate_dcf(invalid)
