from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from services.valuation import (
    CapitalMarketAssumptions,
    ForecastProfile,
    build_valuation_snapshot,
    run_dcf_from_research,
)


@dataclass
class ValuationWorkspaceState:
    ticker: str
    snapshot: dict[str, Any]
    forecast_profile: dict[str, Any]
    capital_market_assumptions: dict[str, Any]
    result: dict[str, Any] | None = None
    errors: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_default_workspace(
    research: dict[str, Any],
) -> ValuationWorkspaceState:
    snapshot = build_valuation_snapshot(research)

    default_growth = [0.20, 0.25, 0.30, 0.28, 0.22]
    default_margins = [-5.50, -3.50, -2.00, -0.75, 0.05]

    return ValuationWorkspaceState(
        ticker=snapshot.ticker,
        snapshot=snapshot.to_dict(),
        forecast_profile={
            "revenue_growth_rates": default_growth,
            "ebit_margins": default_margins,
            "tax_rate": 0.21,
            "depreciation_amortization_pct_revenue": 0.06,
            "capex_pct_revenue": 0.08,
            "nwc_pct_revenue_change": 0.05,
            "terminal_growth_rate": 0.025,
            "source": "Analyst-edited assumptions",
            "note": "Review before use.",
        },
        capital_market_assumptions={
            "risk_free_rate": 0.04,
            "equity_risk_premium": 0.055,
            "cost_of_debt": 0.07,
            "debt_weight": 0.05,
            "equity_weight": 0.95,
            "beta_override": None,
            "source": "Analyst-edited assumptions",
            "note": "Review before use.",
        },
        result=None,
        errors=[],
    )


def run_workspace_valuation(
    research: dict[str, Any],
    workspace: ValuationWorkspaceState,
) -> ValuationWorkspaceState:
    try:
        forecast = ForecastProfile(
            **workspace.forecast_profile,
        )

        capital = CapitalMarketAssumptions(
            **workspace.capital_market_assumptions,
        )

        result = run_dcf_from_research(
            research=research,
            forecast_profile=forecast,
            capital_market_assumptions=capital,
            sensitivity_wacc_values=[
                0.09,
                0.10,
                0.11,
                0.12,
                0.13,
            ],
            sensitivity_terminal_growth_values=[
                0.01,
                0.015,
                0.02,
                0.025,
                0.03,
            ],
        )

        workspace.result = result
        workspace.errors = []

    except Exception as exc:
        workspace.result = None
        workspace.errors = [
            f"{type(exc).__name__}: {exc}"
        ]

    return workspace
