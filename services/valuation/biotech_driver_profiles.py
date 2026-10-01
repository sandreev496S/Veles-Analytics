from __future__ import annotations

from services.valuation.models import (
    BiotechDriverAssumptions,
    ValuationDataSnapshot,
)


def _require(snapshot_input, name: str) -> float:
    if snapshot_input.value is None:
        raise ValueError(
            f"Missing required valuation input: {name}"
        )

    return float(snapshot_input.value)


def build_biotech_driver_profile(
    snapshot: ValuationDataSnapshot,
    *,
    forecast_years: int = 10,
    risk_free_rate: float = 0.04,
    equity_risk_premium: float = 0.055,
    cost_of_debt: float = 0.07,
    debt_weight: float = 0.05,
    terminal_growth_rate: float = 0.025,
) -> BiotechDriverAssumptions:
    if forecast_years not in {10, 15}:
        raise ValueError(
            "forecast_years must be either 10 or 15."
        )

    base_revenue = _require(
        snapshot.base_revenue,
        "Base Revenue",
    )

    cash = _require(snapshot.cash, "Cash")
    debt = _require(snapshot.debt, "Debt")
    beta = _require(snapshot.beta, "Beta")
    shares = _require(
        snapshot.diluted_shares_outstanding,
        "Diluted Shares",
    )

    # Until revenue segmentation is connected, all observed revenue is
    # classified as collaboration/platform revenue.
    base_collaboration_revenue = base_revenue

    collaboration_growth_10 = [
        0.20,
        0.22,
        0.24,
        0.22,
        0.18,
        0.15,
        0.12,
        0.10,
        0.08,
        0.06,
    ]

    product_revenue_10 = [
        0,
        0,
        0,
        0,
        25_000_000,
        80_000_000,
        180_000_000,
        350_000_000,
        550_000_000,
        750_000_000,
    ]

    milestone_revenue_10 = [
        20_000_000,
        25_000_000,
        35_000_000,
        50_000_000,
        65_000_000,
        80_000_000,
        95_000_000,
        110_000_000,
        125_000_000,
        140_000_000,
    ]

    rd_10 = [
        500_000_000,
        520_000_000,
        535_000_000,
        545_000_000,
        550_000_000,
        545_000_000,
        525_000_000,
        500_000_000,
        475_000_000,
        450_000_000,
    ]

    sga_10 = [
        145_000_000,
        150_000_000,
        155_000_000,
        165_000_000,
        175_000_000,
        190_000_000,
        210_000_000,
        235_000_000,
        260_000_000,
        285_000_000,
    ]

    other_10 = [
        20_000_000,
        20_000_000,
        20_000_000,
        20_000_000,
        20_000_000,
        20_000_000,
        20_000_000,
        20_000_000,
        20_000_000,
        20_000_000,
    ]

    if forecast_years == 15:
        collaboration_growth = (
            collaboration_growth_10
            + [0.05, 0.045, 0.04, 0.035, 0.03]
        )
        product_revenue = (
            product_revenue_10
            + [
                950_000_000,
                1_150_000_000,
                1_350_000_000,
                1_550_000_000,
                1_750_000_000,
            ]
        )
        milestone_revenue = (
            milestone_revenue_10
            + [
                150_000_000,
                160_000_000,
                170_000_000,
                180_000_000,
                190_000_000,
            ]
        )
        rd = (
            rd_10
            + [
                440_000_000,
                430_000_000,
                425_000_000,
                420_000_000,
                415_000_000,
            ]
        )
        sga = (
            sga_10
            + [
                310_000_000,
                335_000_000,
                360_000_000,
                385_000_000,
                410_000_000,
            ]
        )
        other = other_10 + [20_000_000] * 5
    else:
        collaboration_growth = collaboration_growth_10
        product_revenue = product_revenue_10
        milestone_revenue = milestone_revenue_10
        rd = rd_10
        sga = sga_10
        other = other_10

    return BiotechDriverAssumptions(
        ticker=snapshot.ticker,
        base_year=snapshot.base_year or 2025,
        base_collaboration_revenue=(
            base_collaboration_revenue
        ),
        base_product_revenue=0.0,
        base_milestone_revenue=0.0,
        collaboration_growth_rates=(
            collaboration_growth
        ),
        product_revenue_forecast=product_revenue,
        milestone_revenue_forecast=(
            milestone_revenue
        ),
        research_and_development_forecast=rd,
        selling_general_admin_forecast=sga,
        other_operating_expense_forecast=other,
        tax_rate=0.21,
        depreciation_amortization_pct_revenue=0.05,
        capex_pct_revenue=0.06,
        nwc_pct_revenue_change=0.04,
        risk_free_rate=risk_free_rate,
        equity_risk_premium=equity_risk_premium,
        beta=beta,
        cost_of_debt=cost_of_debt,
        debt_weight=debt_weight,
        equity_weight=1.0 - debt_weight,
        terminal_growth_rate=terminal_growth_rate,
        cash=cash,
        debt=debt,
        diluted_shares_outstanding=shares,
        scenario_name="Base",
        model_status="illustrative",
        model_note=(
            f"Illustrative {forecast_years}-year driver-based "
            "biotechnology scenario. Inputs require analyst review "
            "and do not represent a final investment valuation."
        ),
    )
