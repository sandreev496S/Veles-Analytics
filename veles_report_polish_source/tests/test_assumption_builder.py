import pytest

from services.valuation import (
    CapitalMarketAssumptions,
    ForecastProfile,
    ValuationDataSnapshot,
    ValuationInput,
    ValuationInputError,
    build_dcf_assumptions,
)


def observed(
    name: str,
    value: float | None,
    unit: str = "USD",
) -> ValuationInput:
    return ValuationInput(
        name=name,
        value=value,
        unit=unit,
        source="Test source",
        source_key=name,
        status=(
            "observed"
            if value is not None
            else "missing"
        ),
    )


def snapshot() -> ValuationDataSnapshot:
    return ValuationDataSnapshot(
        ticker="TEST",
        base_year=2025,
        base_revenue=observed(
            "Base Revenue",
            100_000_000,
        ),
        cash=observed(
            "Cash",
            250_000_000,
        ),
        debt=observed(
            "Debt",
            50_000_000,
        ),
        beta=observed(
            "Beta",
            1.2,
            "multiple",
        ),
        market_cap=observed(
            "Market Cap",
            1_000_000_000,
        ),
        enterprise_value=observed(
            "Enterprise Value",
            800_000_000,
        ),
        diluted_shares_outstanding=ValuationInput(
            name="Diluted Shares",
            value=100_000_000,
            unit="shares",
            source="Derived",
            source_key="Market Cap / Share Price",
            status="derived",
        ),
        share_price=observed(
            "Share Price",
            10.0,
            "USD/share",
        ),
    )


def profile() -> ForecastProfile:
    return ForecastProfile(
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
        terminal_growth_rate=0.025,
    )


def markets() -> CapitalMarketAssumptions:
    return CapitalMarketAssumptions(
        risk_free_rate=0.04,
        equity_risk_premium=0.055,
        cost_of_debt=0.07,
        debt_weight=0.10,
        equity_weight=0.90,
    )


def test_builder_uses_observed_inputs():
    result = build_dcf_assumptions(
        snapshot(),
        profile(),
        markets(),
    )

    assumptions = result.assumptions

    assert assumptions.base_revenue == 100_000_000
    assert assumptions.cash == 250_000_000
    assert assumptions.debt == 50_000_000
    assert assumptions.beta == 1.2
    assert assumptions.diluted_shares_outstanding == 100_000_000


def test_builder_preserves_input_provenance():
    result = build_dcf_assumptions(
        snapshot(),
        profile(),
        markets(),
    )

    assert (
        result.observed_inputs["base_revenue"]["source"]
        == "Test source"
    )
    assert (
        result.analyst_inputs["forecast_profile"]["source"]
        == "Analyst-provided assumptions"
    )


def test_builder_requires_revenue():
    missing = snapshot()
    missing.base_revenue = observed(
        "Base Revenue",
        None,
    )

    with pytest.raises(ValuationInputError):
        build_dcf_assumptions(
            missing,
            profile(),
            markets(),
        )


def test_beta_override_replaces_observed_beta():
    capital = CapitalMarketAssumptions(
        risk_free_rate=0.04,
        equity_risk_premium=0.055,
        cost_of_debt=0.07,
        debt_weight=0.10,
        equity_weight=0.90,
        beta_override=1.5,
    )

    result = build_dcf_assumptions(
        snapshot(),
        profile(),
        capital,
    )

    assert result.assumptions.beta == 1.5
    assert any(
        "beta override" in warning.lower()
        for warning in result.warnings
    )
