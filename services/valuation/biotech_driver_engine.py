from __future__ import annotations

from dataclasses import replace

from services.valuation.models import (
    BiotechDriverAssumptions,
    BiotechDriverDCFResult,
    BiotechDriverYear,
)


class BiotechDriverInputError(ValueError):
    pass


def _forecast_length(
    assumptions: BiotechDriverAssumptions,
) -> int:
    lengths = {
        len(assumptions.collaboration_growth_rates),
        len(assumptions.product_revenue_forecast),
        len(assumptions.milestone_revenue_forecast),
        len(assumptions.research_and_development_forecast),
        len(assumptions.selling_general_admin_forecast),
        len(assumptions.other_operating_expense_forecast),
    }

    if len(lengths) != 1:
        raise BiotechDriverInputError(
            "All biotech driver forecast arrays must have equal lengths."
        )

    years = lengths.pop()

    if years not in {10, 15}:
        raise BiotechDriverInputError(
            "Driver-based biotech forecasts must contain 10 or 15 years."
        )

    return years


def validate_biotech_driver_assumptions(
    assumptions: BiotechDriverAssumptions,
) -> list[str]:
    _forecast_length(assumptions)

    errors: list[str] = []
    warnings: list[str] = []

    if assumptions.diluted_shares_outstanding <= 0:
        errors.append(
            "Diluted shares outstanding must be greater than zero."
        )

    if assumptions.cash < 0 or assumptions.debt < 0:
        errors.append("Cash and debt cannot be negative.")

    if abs(
        assumptions.debt_weight
        + assumptions.equity_weight
        - 1.0
    ) > 0.0001:
        errors.append(
            "Debt and equity weights must sum to 1.0."
        )

    cost_of_equity = (
        assumptions.risk_free_rate
        + assumptions.beta
        * assumptions.equity_risk_premium
    )

    after_tax_debt = (
        assumptions.cost_of_debt
        * (1 - assumptions.tax_rate)
    )

    wacc = (
        assumptions.equity_weight * cost_of_equity
        + assumptions.debt_weight * after_tax_debt
    )

    if wacc <= assumptions.terminal_growth_rate:
        errors.append(
            "WACC must be greater than terminal growth."
        )

    if any(
        value < 0
        for value in (
            assumptions.research_and_development_forecast
            + assumptions.selling_general_admin_forecast
            + assumptions.other_operating_expense_forecast
        )
    ):
        errors.append(
            "Operating-expense forecasts cannot be negative."
        )

    if assumptions.model_status == "illustrative":
        warnings.append(
            "This is an illustrative scenario model, not a final valuation."
        )

    if errors:
        raise BiotechDriverInputError(" ".join(errors))

    return warnings


def calculate_biotech_driver_dcf(
    assumptions: BiotechDriverAssumptions,
) -> BiotechDriverDCFResult:
    warnings = validate_biotech_driver_assumptions(
        assumptions
    )

    cost_of_equity = (
        assumptions.risk_free_rate
        + assumptions.beta
        * assumptions.equity_risk_premium
    )

    after_tax_cost_of_debt = (
        assumptions.cost_of_debt
        * (1 - assumptions.tax_rate)
    )

    wacc = (
        assumptions.equity_weight * cost_of_equity
        + assumptions.debt_weight
        * after_tax_cost_of_debt
    )

    forecast: list[BiotechDriverYear] = []

    prior_collaboration = (
        assumptions.base_collaboration_revenue
    )
    prior_total_revenue = (
        assumptions.base_collaboration_revenue
        + assumptions.base_product_revenue
        + assumptions.base_milestone_revenue
    )

    for index in range(
        len(assumptions.collaboration_growth_rates)
    ):
        year = assumptions.base_year + index + 1

        collaboration_revenue = (
            prior_collaboration
            * (
                1
                + assumptions.collaboration_growth_rates[
                    index
                ]
            )
        )

        product_revenue = (
            assumptions.product_revenue_forecast[index]
        )
        milestone_revenue = (
            assumptions.milestone_revenue_forecast[index]
        )

        total_revenue = (
            collaboration_revenue
            + product_revenue
            + milestone_revenue
        )

        revenue_growth = (
            total_revenue / prior_total_revenue - 1
            if prior_total_revenue > 0
            else 0.0
        )

        research_and_development = (
            assumptions.research_and_development_forecast[
                index
            ]
        )
        selling_general_admin = (
            assumptions.selling_general_admin_forecast[
                index
            ]
        )
        other_operating_expense = (
            assumptions.other_operating_expense_forecast[
                index
            ]
        )

        total_operating_expense = (
            research_and_development
            + selling_general_admin
            + other_operating_expense
        )

        ebit = total_revenue - total_operating_expense

        ebit_margin = (
            ebit / total_revenue
            if total_revenue > 0
            else 0.0
        )

        effective_tax_rate = (
            assumptions.tax_rate if ebit > 0 else 0.0
        )

        nopat = ebit * (1 - effective_tax_rate)

        depreciation_amortization = (
            total_revenue
            * assumptions.depreciation_amortization_pct_revenue
        )

        capital_expenditures = (
            total_revenue
            * assumptions.capex_pct_revenue
        )

        revenue_change = (
            total_revenue - prior_total_revenue
        )

        change_in_nwc = (
            revenue_change
            * assumptions.nwc_pct_revenue_change
        )

        unlevered_fcf = (
            nopat
            + depreciation_amortization
            - capital_expenditures
            - change_in_nwc
        )

        discount_factor = 1 / (
            (1 + wacc) ** (index + 1)
        )

        present_value_fcf = (
            unlevered_fcf * discount_factor
        )

        forecast.append(
            BiotechDriverYear(
                year=year,
                collaboration_revenue=collaboration_revenue,
                product_revenue=product_revenue,
                milestone_revenue=milestone_revenue,
                total_revenue=total_revenue,
                revenue_growth=revenue_growth,
                research_and_development=(
                    research_and_development
                ),
                selling_general_admin=(
                    selling_general_admin
                ),
                other_operating_expense=(
                    other_operating_expense
                ),
                total_operating_expense=(
                    total_operating_expense
                ),
                ebit=ebit,
                ebit_margin=ebit_margin,
                tax_rate=effective_tax_rate,
                nopat=nopat,
                depreciation_amortization=(
                    depreciation_amortization
                ),
                capital_expenditures=(
                    capital_expenditures
                ),
                change_in_nwc=change_in_nwc,
                unlevered_fcf=unlevered_fcf,
                discount_factor=discount_factor,
                present_value_fcf=present_value_fcf,
            )
        )

        prior_collaboration = collaboration_revenue
        prior_total_revenue = total_revenue

    terminal_ebit_margin = forecast[-1].ebit_margin

    if terminal_ebit_margin > 0.40:
        warnings.append(
            "Terminal-year EBIT margin exceeds 40%. "
            "Review mature-state revenue and operating-expense assumptions."
        )

    final_fcf = forecast[-1].unlevered_fcf

    if final_fcf <= 0:
        warnings.append(
            "Terminal-year free cash flow is non-positive; "
            "the perpetuity terminal value may not be economically meaningful."
        )

    terminal_value = (
        final_fcf
        * (1 + assumptions.terminal_growth_rate)
        / (wacc - assumptions.terminal_growth_rate)
    )

    present_value_terminal_value = (
        terminal_value
        * forecast[-1].discount_factor
    )

    present_value_forecast_fcf = sum(
        item.present_value_fcf
        for item in forecast
    )

    enterprise_value = (
        present_value_forecast_fcf
        + present_value_terminal_value
    )

    net_debt = assumptions.debt - assumptions.cash
    equity_value = enterprise_value - net_debt

    implied_value_per_share = (
        equity_value
        / assumptions.diluted_shares_outstanding
    )

    if enterprise_value < 0:
        warnings.append(
            "Modeled enterprise value is negative under the selected assumptions."
        )

    if equity_value < 0:
        warnings.append(
            "Modeled equity value is negative. The professional report "
            "will display a zero-floor value while preserving the raw result."
        )

    return BiotechDriverDCFResult(
        ticker=assumptions.ticker,
        scenario_name=assumptions.scenario_name,
        forecast=forecast,
        cost_of_equity=cost_of_equity,
        after_tax_cost_of_debt=after_tax_cost_of_debt,
        wacc=wacc,
        terminal_value=terminal_value,
        present_value_terminal_value=(
            present_value_terminal_value
        ),
        present_value_forecast_fcf=(
            present_value_forecast_fcf
        ),
        enterprise_value=enterprise_value,
        net_debt=net_debt,
        equity_value=equity_value,
        implied_value_per_share=(
            implied_value_per_share
        ),
        assumptions=assumptions,
        warnings=warnings,
    )


def build_biotech_driver_scenarios(
    base: BiotechDriverAssumptions,
) -> dict[str, BiotechDriverAssumptions]:
    bull = replace(
        base,
        scenario_name="Bull",
        collaboration_growth_rates=[
            growth + 0.03
            for growth in base.collaboration_growth_rates
        ],
        product_revenue_forecast=[
            value * 1.25
            for value in base.product_revenue_forecast
        ],
        milestone_revenue_forecast=[
            value * 1.20
            for value in base.milestone_revenue_forecast
        ],
        research_and_development_forecast=[
            value * 0.95
            for value in base.research_and_development_forecast
        ],
        terminal_growth_rate=min(
            base.terminal_growth_rate + 0.005,
            0.04,
        ),
        equity_risk_premium=max(
            base.equity_risk_premium - 0.005,
            0.01,
        ),
    )

    bear = replace(
        base,
        scenario_name="Bear",
        collaboration_growth_rates=[
            growth - 0.03
            for growth in base.collaboration_growth_rates
        ],
        product_revenue_forecast=[
            value * 0.70
            for value in base.product_revenue_forecast
        ],
        milestone_revenue_forecast=[
            value * 0.70
            for value in base.milestone_revenue_forecast
        ],
        research_and_development_forecast=[
            value * 1.10
            for value in base.research_and_development_forecast
        ],
        selling_general_admin_forecast=[
            value * 1.05
            for value in base.selling_general_admin_forecast
        ],
        terminal_growth_rate=max(
            base.terminal_growth_rate - 0.005,
            0.0,
        ),
        equity_risk_premium=(
            base.equity_risk_premium + 0.01
        ),
    )

    return {
        "bull": bull,
        "base": replace(base, scenario_name="Base"),
        "bear": bear,
    }


def calculate_biotech_driver_scenarios(
    base: BiotechDriverAssumptions,
) -> dict[str, BiotechDriverDCFResult]:
    results = {
        name: calculate_biotech_driver_dcf(
            assumptions
        )
        for name, assumptions
        in build_biotech_driver_scenarios(base).items()
    }

    bull_value = results[
        "bull"
    ].implied_value_per_share
    base_value = results[
        "base"
    ].implied_value_per_share
    bear_value = results[
        "bear"
    ].implied_value_per_share

    if not (
        bull_value >= base_value >= bear_value
    ):
        raise BiotechDriverInputError(
            "Scenario monotonicity validation failed: "
            f"Bull={bull_value:.4f}, "
            f"Base={base_value:.4f}, "
            f"Bear={bear_value:.4f}. "
            "Bull must be greater than or equal to Base, "
            "and Base must be greater than or equal to Bear."
        )

    return results
