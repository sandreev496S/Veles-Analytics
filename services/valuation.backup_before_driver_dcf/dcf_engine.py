from __future__ import annotations

from dataclasses import replace

from services.valuation.models import (
    DCFAssumptions,
    DCFResult,
    ForecastYear,
    SensitivityCell,
    SensitivityResult,
)
from services.valuation.validation import validate_dcf_assumptions


def calculate_cost_of_equity(
    risk_free_rate: float,
    beta: float,
    equity_risk_premium: float,
) -> float:
    return risk_free_rate + beta * equity_risk_premium


def calculate_wacc(
    assumptions: DCFAssumptions,
) -> tuple[float, float, float]:
    cost_of_equity = calculate_cost_of_equity(
        risk_free_rate=assumptions.risk_free_rate,
        beta=assumptions.beta,
        equity_risk_premium=assumptions.equity_risk_premium,
    )

    after_tax_cost_of_debt = (
        assumptions.cost_of_debt
        * (1 - assumptions.tax_rate)
    )

    wacc = (
        assumptions.equity_weight * cost_of_equity
        + assumptions.debt_weight * after_tax_cost_of_debt
    )

    return cost_of_equity, after_tax_cost_of_debt, wacc


def calculate_dcf(
    assumptions: DCFAssumptions,
) -> DCFResult:
    warnings = validate_dcf_assumptions(assumptions)

    cost_of_equity, after_tax_cost_of_debt, wacc = calculate_wacc(
        assumptions
    )

    forecast: list[ForecastYear] = []
    prior_revenue = assumptions.base_revenue

    for index, (
        revenue_growth,
        ebit_margin,
    ) in enumerate(
        zip(
            assumptions.revenue_growth_rates,
            assumptions.ebit_margins,
        ),
        start=1,
    ):
        year = assumptions.base_year + index
        revenue = prior_revenue * (1 + revenue_growth)
        ebit = revenue * ebit_margin

        # Apply cash taxes only when EBIT is positive.
        effective_tax_rate = (
            assumptions.tax_rate
            if ebit > 0
            else 0.0
        )

        nopat = ebit * (1 - effective_tax_rate)

        depreciation_amortization = (
            revenue
            * assumptions.depreciation_amortization_pct_revenue
        )

        capital_expenditures = (
            revenue * assumptions.capex_pct_revenue
        )

        revenue_change = revenue - prior_revenue

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

        discount_factor = 1 / ((1 + wacc) ** index)
        present_value_fcf = unlevered_fcf * discount_factor

        forecast.append(
            ForecastYear(
                year=year,
                revenue=revenue,
                revenue_growth=revenue_growth,
                ebit_margin=ebit_margin,
                ebit=ebit,
                tax_rate=effective_tax_rate,
                nopat=nopat,
                depreciation_amortization=depreciation_amortization,
                capital_expenditures=capital_expenditures,
                change_in_nwc=change_in_nwc,
                unlevered_fcf=unlevered_fcf,
                discount_factor=discount_factor,
                present_value_fcf=present_value_fcf,
            )
        )

        prior_revenue = revenue

    final_fcf = forecast[-1].unlevered_fcf

    terminal_value = (
        final_fcf
        * (1 + assumptions.terminal_growth_rate)
        / (wacc - assumptions.terminal_growth_rate)
    )

    terminal_discount_factor = forecast[-1].discount_factor

    present_value_terminal_value = (
        terminal_value * terminal_discount_factor
    )

    present_value_forecast_fcf = sum(
        year.present_value_fcf
        for year in forecast
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

    if terminal_value < 0:
        warnings.append(
            "Terminal value is negative because terminal-year FCF is negative."
        )

    terminal_value_share = (
        present_value_terminal_value / enterprise_value
        if enterprise_value
        else 0
    )

    if terminal_value_share > 0.85:
        warnings.append(
            "More than 85% of enterprise value comes from terminal value."
        )

    return DCFResult(
        ticker=assumptions.ticker,
        scenario_name=assumptions.scenario_name,
        forecast=forecast,
        cost_of_equity=cost_of_equity,
        after_tax_cost_of_debt=after_tax_cost_of_debt,
        wacc=wacc,
        terminal_value=terminal_value,
        present_value_terminal_value=present_value_terminal_value,
        present_value_forecast_fcf=present_value_forecast_fcf,
        enterprise_value=enterprise_value,
        net_debt=net_debt,
        equity_value=equity_value,
        implied_value_per_share=implied_value_per_share,
        assumptions=assumptions,
        warnings=warnings,
    )


def calculate_sensitivity(
    assumptions: DCFAssumptions,
    wacc_values: list[float],
    terminal_growth_values: list[float],
) -> SensitivityResult:
    cells: list[SensitivityCell] = []

    for wacc in wacc_values:
        for terminal_growth in terminal_growth_values:
            if wacc <= terminal_growth:
                continue

            # Derive a cost-of-equity input that produces the requested WACC
            # while preserving debt weight and after-tax debt cost.
            after_tax_debt_cost = (
                assumptions.cost_of_debt
                * (1 - assumptions.tax_rate)
            )

            implied_cost_of_equity = (
                wacc
                - assumptions.debt_weight * after_tax_debt_cost
            ) / assumptions.equity_weight

            implied_erp = (
                implied_cost_of_equity
                - assumptions.risk_free_rate
            ) / assumptions.beta

            scenario_assumptions = replace(
                assumptions,
                equity_risk_premium=implied_erp,
                terminal_growth_rate=terminal_growth,
                scenario_name=(
                    f"WACC {wacc:.1%} / "
                    f"Terminal Growth {terminal_growth:.1%}"
                ),
            )

            result = calculate_dcf(scenario_assumptions)

            cells.append(
                SensitivityCell(
                    wacc=wacc,
                    terminal_growth_rate=terminal_growth,
                    enterprise_value=result.enterprise_value,
                    equity_value=result.equity_value,
                    implied_value_per_share=(
                        result.implied_value_per_share
                    ),
                )
            )

    return SensitivityResult(
        wacc_values=wacc_values,
        terminal_growth_values=terminal_growth_values,
        cells=cells,
    )
