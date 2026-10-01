from __future__ import annotations

from services.valuation.models import DCFAssumptions


class ValuationInputError(ValueError):
    pass


def validate_dcf_assumptions(
    assumptions: DCFAssumptions,
) -> list[str]:
    errors: list[str] = []
    warnings: list[str] = []

    forecast_years = len(assumptions.revenue_growth_rates)

    if forecast_years == 0:
        errors.append("At least one forecast year is required.")

    if len(assumptions.ebit_margins) != forecast_years:
        errors.append(
            "Revenue growth rates and EBIT margins must have equal lengths."
        )

    if assumptions.base_revenue < 0:
        errors.append("Base revenue cannot be negative.")

    if assumptions.diluted_shares_outstanding <= 0:
        errors.append("Diluted shares outstanding must be greater than zero.")

    if assumptions.cash < 0:
        errors.append("Cash cannot be negative.")

    if assumptions.debt < 0:
        errors.append("Debt cannot be negative.")

    if not 0 <= assumptions.tax_rate <= 1:
        errors.append("Tax rate must be between 0 and 1.")

    if not 0 <= assumptions.debt_weight <= 1:
        errors.append("Debt weight must be between 0 and 1.")

    if not 0 <= assumptions.equity_weight <= 1:
        errors.append("Equity weight must be between 0 and 1.")

    weight_total = assumptions.debt_weight + assumptions.equity_weight

    if abs(weight_total - 1.0) > 0.0001:
        errors.append("Debt and equity weights must sum to 1.0.")

    cost_of_equity = (
        assumptions.risk_free_rate
        + assumptions.beta * assumptions.equity_risk_premium
    )

    estimated_wacc = (
        assumptions.equity_weight * cost_of_equity
        + assumptions.debt_weight
        * assumptions.cost_of_debt
        * (1 - assumptions.tax_rate)
    )

    if estimated_wacc <= assumptions.terminal_growth_rate:
        errors.append(
            "WACC must be greater than the terminal growth rate."
        )

    if assumptions.terminal_growth_rate < 0:
        warnings.append("Terminal growth rate is negative.")

    if assumptions.terminal_growth_rate > 0.04:
        warnings.append(
            "Terminal growth exceeds 4%; verify long-term economic plausibility."
        )

    if assumptions.beta <= 0:
        warnings.append("Beta is non-positive; verify the market-risk input.")

    if any(rate > 1 for rate in assumptions.revenue_growth_rates):
        warnings.append(
            "At least one annual revenue growth assumption exceeds 100%."
        )

    if any(margin < -2 or margin > 1 for margin in assumptions.ebit_margins):
        warnings.append(
            "At least one EBIT margin assumption is outside -200% to 100%."
        )

    if errors:
        raise ValuationInputError(" ".join(errors))

    return warnings
