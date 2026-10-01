from __future__ import annotations

from typing import Any

from services.analysis.financial_metrics import (
    build_financial_metrics,
)


def classify_growth(
    growth_pct: float | None,
) -> str:
    if growth_pct is None:
        return "unknown"

    if growth_pct >= 30:
        return "strong"
    if growth_pct >= 10:
        return "moderate"
    if growth_pct > 0:
        return "modest"
    if growth_pct == 0:
        return "flat"
    if growth_pct > -10:
        return "modest_decline"

    return "material_decline"




def _growth_direction(value: float | None) -> str:
    if value is None:
        return "unknown"
    if value > 0:
        return "increase"
    if value < 0:
        return "decline"
    return "flat"


def _absolute_value(value: float | None) -> float | None:
    return abs(value) if value is not None else None


def classify_liquidity(
    *,
    cash: float | None,
    debt: float | None,
    free_cash_flow: float | None,
    estimated_runway: Any,
) -> str:
    """
    Backwards-compatible deterministic liquidity classifier.

    New code should use build_financial_metrics directly.
    """
    metrics = build_financial_metrics(
        cash=cash,
        debt=debt,
        free_cash_flow=free_cash_flow,
        estimated_runway=estimated_runway,
    )

    return metrics.liquidity_state.value


def classify_profitability(
    *,
    net_income: float | None,
    free_cash_flow: float | None,
) -> str:
    if (
        net_income is not None
        and net_income > 0
        and free_cash_flow is not None
        and free_cash_flow > 0
    ):
        return "profitable_cash_generative"

    if (
        net_income is not None
        and net_income > 0
    ):
        return "profitable"

    if (
        net_income is not None
        and net_income < 0
        and free_cash_flow is not None
        and free_cash_flow < 0
    ):
        return "loss_making_cash_burning"

    if net_income is not None and net_income < 0:
        return "loss_making"

    return "unknown"


def classify_rd_intensity(
    *,
    rd_expense: float | None,
    revenue: float | None,
) -> str:
    if rd_expense is None:
        return "unknown"

    if revenue is None or revenue <= 0:
        return "high"

    ratio = rd_expense / revenue

    if ratio >= 2:
        return "very_high"
    if ratio >= 0.5:
        return "high"
    if ratio >= 0.15:
        return "moderate"

    return "low"


def build_financial_assessment(
    *,
    revenue_growth: float | None,
    rd_growth: float | None,
    latest_revenue: float | None,
    latest_rd: float | None,
    cash: float | None,
    debt: float | None,
    free_cash_flow: float | None,
    net_income: float | None,
    estimated_runway: Any,
    market_cap: float | None = None,
    enterprise_value: float | None = None,
) -> dict[str, Any]:
    metrics = build_financial_metrics(
        cash=cash,
        debt=debt,
        market_cap=market_cap,
        enterprise_value=enterprise_value,
        free_cash_flow=free_cash_flow,
        estimated_runway=estimated_runway,
    )

    return {
        "financial_metrics": metrics,
        "revenue": {
            "classification": classify_growth(
                revenue_growth
            ),
            "growth_pct": revenue_growth,
            "absolute_growth_pct": _absolute_value(revenue_growth),
            "direction": _growth_direction(revenue_growth),
            "latest_value": latest_revenue,
        },
        "research_investment": {
            "classification": classify_rd_intensity(
                rd_expense=latest_rd,
                revenue=latest_revenue,
            ),
            "growth_classification": classify_growth(
                rd_growth
            ),
            "growth_pct": rd_growth,
            "absolute_growth_pct": _absolute_value(rd_growth),
            "direction": _growth_direction(rd_growth),
            "latest_value": latest_rd,
        },
        "liquidity": {
            **metrics.to_dict(),
            "classification": metrics.liquidity_state.value,
            "estimated_runway": estimated_runway,
            "runway_available": estimated_runway not in {
                None,
                "",
                "N/A",
                "None",
            },
            "balance_sheet_risk": (
                "debt_exceeds_cash"
                if metrics.balance_sheet_state.value
                == "net_debt"
                else "none"
                if metrics.balance_sheet_state.value
                in {"net_cash", "neutral"}
                else "unknown"
            ),
        },
        "profitability": {
            "classification": classify_profitability(
                net_income=net_income,
                free_cash_flow=free_cash_flow,
            ),
            "net_income": net_income,
            "free_cash_flow": free_cash_flow,
            "cash_flow_state": (
                "cash_burning"
                if free_cash_flow is not None
                and free_cash_flow < 0
                else "cash_generative"
                if free_cash_flow is not None
                and free_cash_flow > 0
                else "neutral"
                if free_cash_flow == 0
                else "unknown"
            ),
            "free_cash_flow_magnitude": _absolute_value(free_cash_flow),
        },
    }
