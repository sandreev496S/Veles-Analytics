from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any

from services.valuation.models import (
    DCFAssumptions,
    ValuationDataSnapshot,
)
from services.valuation.validation import (
    ValuationInputError,
    validate_dcf_assumptions,
)


@dataclass(frozen=True)
class ForecastProfile:
    revenue_growth_rates: list[float]
    ebit_margins: list[float]

    tax_rate: float = 0.21
    depreciation_amortization_pct_revenue: float = 0.04
    capex_pct_revenue: float = 0.05
    nwc_pct_revenue_change: float = 0.08

    terminal_growth_rate: float = 0.025

    source: str = "Analyst-provided assumptions"
    note: str = ""


@dataclass(frozen=True)
class CapitalMarketAssumptions:
    risk_free_rate: float
    equity_risk_premium: float
    cost_of_debt: float

    debt_weight: float
    equity_weight: float

    beta_override: float | None = None

    source: str = "Analyst-provided capital market assumptions"
    note: str = ""


@dataclass
class AssumptionBuildResult:
    assumptions: DCFAssumptions
    observed_inputs: dict[str, dict[str, Any]]
    analyst_inputs: dict[str, Any]
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "assumptions": self.assumptions.__dict__,
            "observed_inputs": self.observed_inputs,
            "analyst_inputs": self.analyst_inputs,
            "warnings": self.warnings,
        }


def _require_value(
    snapshot: ValuationDataSnapshot,
    field_name: str,
) -> float:
    valuation_input = getattr(snapshot, field_name)

    if valuation_input.value is None:
        raise ValuationInputError(
            f"Required valuation input is missing: {valuation_input.name}."
        )

    return valuation_input.value


def _input_record(value) -> dict[str, Any]:
    return {
        "value": value.value,
        "unit": value.unit,
        "source": value.source,
        "source_key": value.source_key,
        "status": value.status,
        "note": value.note,
    }


def build_dcf_assumptions(
    snapshot: ValuationDataSnapshot,
    forecast_profile: ForecastProfile,
    capital_market_assumptions: CapitalMarketAssumptions,
    *,
    scenario_name: str = "Base",
) -> AssumptionBuildResult:
    base_revenue = _require_value(
        snapshot,
        "base_revenue",
    )
    cash = _require_value(
        snapshot,
        "cash",
    )
    debt = _require_value(
        snapshot,
        "debt",
    )
    shares = _require_value(
        snapshot,
        "diluted_shares_outstanding",
    )

    if snapshot.base_year is None:
        raise ValuationInputError(
            "A base financial year is required for the DCF forecast."
        )

    beta = (
        capital_market_assumptions.beta_override
        if capital_market_assumptions.beta_override is not None
        else snapshot.beta.value
    )

    if beta is None:
        raise ValuationInputError(
            "Beta is missing. Supply a beta_override in capital market assumptions."
        )

    assumptions = DCFAssumptions(
        ticker=snapshot.ticker,
        base_year=snapshot.base_year,
        base_revenue=base_revenue,
        revenue_growth_rates=list(
            forecast_profile.revenue_growth_rates
        ),
        ebit_margins=list(
            forecast_profile.ebit_margins
        ),
        tax_rate=forecast_profile.tax_rate,
        depreciation_amortization_pct_revenue=(
            forecast_profile.depreciation_amortization_pct_revenue
        ),
        capex_pct_revenue=forecast_profile.capex_pct_revenue,
        nwc_pct_revenue_change=(
            forecast_profile.nwc_pct_revenue_change
        ),
        risk_free_rate=(
            capital_market_assumptions.risk_free_rate
        ),
        equity_risk_premium=(
            capital_market_assumptions.equity_risk_premium
        ),
        beta=beta,
        cost_of_debt=(
            capital_market_assumptions.cost_of_debt
        ),
        debt_weight=(
            capital_market_assumptions.debt_weight
        ),
        equity_weight=(
            capital_market_assumptions.equity_weight
        ),
        terminal_growth_rate=(
            forecast_profile.terminal_growth_rate
        ),
        cash=cash,
        debt=debt,
        diluted_shares_outstanding=shares,
        valuation_date=date.today().isoformat(),
        scenario_name=scenario_name,
    )

    validation_warnings = validate_dcf_assumptions(
        assumptions
    )

    observed_inputs = {
        "base_revenue": _input_record(
            snapshot.base_revenue
        ),
        "cash": _input_record(snapshot.cash),
        "debt": _input_record(snapshot.debt),
        "beta": _input_record(snapshot.beta),
        "market_cap": _input_record(
            snapshot.market_cap
        ),
        "enterprise_value": _input_record(
            snapshot.enterprise_value
        ),
        "diluted_shares_outstanding": _input_record(
            snapshot.diluted_shares_outstanding
        ),
        "share_price": _input_record(
            snapshot.share_price
        ),
    }

    analyst_inputs = {
        "forecast_profile": {
            "revenue_growth_rates": (
                forecast_profile.revenue_growth_rates
            ),
            "ebit_margins": (
                forecast_profile.ebit_margins
            ),
            "tax_rate": forecast_profile.tax_rate,
            "depreciation_amortization_pct_revenue": (
                forecast_profile.depreciation_amortization_pct_revenue
            ),
            "capex_pct_revenue": (
                forecast_profile.capex_pct_revenue
            ),
            "nwc_pct_revenue_change": (
                forecast_profile.nwc_pct_revenue_change
            ),
            "terminal_growth_rate": (
                forecast_profile.terminal_growth_rate
            ),
            "source": forecast_profile.source,
            "note": forecast_profile.note,
        },
        "capital_market_assumptions": {
            "risk_free_rate": (
                capital_market_assumptions.risk_free_rate
            ),
            "equity_risk_premium": (
                capital_market_assumptions.equity_risk_premium
            ),
            "cost_of_debt": (
                capital_market_assumptions.cost_of_debt
            ),
            "debt_weight": (
                capital_market_assumptions.debt_weight
            ),
            "equity_weight": (
                capital_market_assumptions.equity_weight
            ),
            "beta_override": (
                capital_market_assumptions.beta_override
            ),
            "source": (
                capital_market_assumptions.source
            ),
            "note": capital_market_assumptions.note,
        },
    }

    warnings = [
        *snapshot.warnings,
        *validation_warnings,
    ]

    if (
        snapshot.diluted_shares_outstanding.status
        == "derived"
    ):
        warnings.append(
            "Diluted shares outstanding were inferred from market capitalization divided by share price."
        )

    if capital_market_assumptions.beta_override is not None:
        warnings.append(
            "The observed provider beta was replaced with an analyst beta override."
        )

    return AssumptionBuildResult(
        assumptions=assumptions,
        observed_inputs=observed_inputs,
        analyst_inputs=analyst_inputs,
        warnings=warnings,
    )
