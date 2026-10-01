from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ValuationInput:
    name: str
    value: float | None
    unit: str
    source: str
    source_key: str
    status: str
    note: str = ""


@dataclass
class ValuationDataSnapshot:
    ticker: str
    base_year: int | None
    base_revenue: ValuationInput
    cash: ValuationInput
    debt: ValuationInput
    beta: ValuationInput
    market_cap: ValuationInput
    enterprise_value: ValuationInput
    diluted_shares_outstanding: ValuationInput
    share_price: ValuationInput
    metadata: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ForecastYear:
    year: int
    revenue: float
    revenue_growth: float
    ebit_margin: float
    ebit: float
    tax_rate: float
    nopat: float
    depreciation_amortization: float
    capital_expenditures: float
    change_in_nwc: float
    unlevered_fcf: float
    discount_factor: float
    present_value_fcf: float


@dataclass(frozen=True)
class DCFAssumptions:
    ticker: str
    base_year: int
    base_revenue: float

    revenue_growth_rates: list[float]
    ebit_margins: list[float]

    tax_rate: float
    depreciation_amortization_pct_revenue: float
    capex_pct_revenue: float
    nwc_pct_revenue_change: float

    risk_free_rate: float
    equity_risk_premium: float
    beta: float
    cost_of_debt: float
    debt_weight: float
    equity_weight: float

    terminal_growth_rate: float

    cash: float
    debt: float
    diluted_shares_outstanding: float

    valuation_date: str = ""
    scenario_name: str = "Base"


@dataclass
class DCFResult:
    ticker: str
    scenario_name: str
    forecast: list[ForecastYear]

    cost_of_equity: float
    after_tax_cost_of_debt: float
    wacc: float

    terminal_value: float
    present_value_terminal_value: float
    present_value_forecast_fcf: float

    enterprise_value: float
    net_debt: float
    equity_value: float
    implied_value_per_share: float

    assumptions: DCFAssumptions
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SensitivityCell:
    wacc: float
    terminal_growth_rate: float
    enterprise_value: float
    equity_value: float
    implied_value_per_share: float


@dataclass
class SensitivityResult:
    wacc_values: list[float]
    terminal_growth_values: list[float]
    cells: list[SensitivityCell]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
