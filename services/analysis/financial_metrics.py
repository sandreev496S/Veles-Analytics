from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from math import isclose
from typing import Any


class BalanceSheetState(str, Enum):
    NET_CASH = "net_cash"
    NET_DEBT = "net_debt"
    NEUTRAL = "neutral"
    UNKNOWN = "unknown"


class EnterpriseValueRelation(str, Enum):
    ABOVE_MARKET_CAP = "above_market_cap"
    BELOW_MARKET_CAP = "below_market_cap"
    EQUAL = "equal"
    UNKNOWN = "unknown"


class LiquidityState(str, Enum):
    VERY_STRONG = "very_strong"
    STRONG = "strong"
    ADEQUATE = "adequate"
    CONSTRAINED = "constrained"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class FinancialMetrics:
    cash: float | None
    debt: float | None
    net_position: float | None
    balance_sheet_state: BalanceSheetState
    market_cap: float | None
    enterprise_value: float | None
    enterprise_value_relation: EnterpriseValueRelation
    estimated_runway_years: float | None
    liquidity_state: LiquidityState

    @property
    def net_cash(self) -> float | None:
        if self.balance_sheet_state is BalanceSheetState.NET_CASH:
            return self.net_position

        return None

    @property
    def net_debt(self) -> float | None:
        if (
            self.balance_sheet_state is BalanceSheetState.NET_DEBT
            and self.net_position is not None
        ):
            return abs(self.net_position)

        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "cash": self.cash,
            "debt": self.debt,
            "net_position": self.net_position,
            "net_cash": self.net_cash,
            "net_debt": self.net_debt,
            "balance_sheet_state": self.balance_sheet_state.value,
            "market_cap": self.market_cap,
            "enterprise_value": self.enterprise_value,
            "enterprise_value_relation": (
                self.enterprise_value_relation.value
            ),
            "estimated_runway_years": self.estimated_runway_years,
            "liquidity_state": self.liquidity_state.value,
        }


def parse_runway_years(
    estimated_runway: Any,
) -> float | None:
    if isinstance(estimated_runway, bool):
        return None

    if isinstance(estimated_runway, (int, float)):
        value = float(estimated_runway)
        return value if value >= 0 else None

    text = str(estimated_runway or "").strip().lower()

    if not text or text in {
        "n/a",
        "na",
        "none",
        "unknown",
        "not available",
    }:
        return None

    number_text = ""

    for character in text:
        if character.isdigit() or character in {".", "-"}:
            number_text += character
        elif number_text:
            break

    try:
        value = float(number_text)
    except (TypeError, ValueError):
        return None

    if value < 0:
        return None

    if "month" in text:
        return value / 12

    return value


def calculate_net_position(
    *,
    cash: float | None,
    debt: float | None,
) -> float | None:
    if cash is None or debt is None:
        return None

    return cash - debt


def classify_balance_sheet_state(
    net_position: float | None,
    *,
    absolute_tolerance: float = 1.0,
) -> BalanceSheetState:
    if net_position is None:
        return BalanceSheetState.UNKNOWN

    if isclose(
        net_position,
        0.0,
        rel_tol=0.0,
        abs_tol=absolute_tolerance,
    ):
        return BalanceSheetState.NEUTRAL

    if net_position > 0:
        return BalanceSheetState.NET_CASH

    return BalanceSheetState.NET_DEBT


def classify_enterprise_value_relation(
    *,
    enterprise_value: float | None,
    market_cap: float | None,
) -> EnterpriseValueRelation:
    if enterprise_value is None or market_cap is None:
        return EnterpriseValueRelation.UNKNOWN

    if isclose(
        enterprise_value,
        market_cap,
        rel_tol=1e-6,
        abs_tol=1.0,
    ):
        return EnterpriseValueRelation.EQUAL

    if enterprise_value > market_cap:
        return EnterpriseValueRelation.ABOVE_MARKET_CAP

    return EnterpriseValueRelation.BELOW_MARKET_CAP


def classify_liquidity_state(
    *,
    balance_sheet_state: BalanceSheetState,
    estimated_runway_years: float | None,
    free_cash_flow: float | None,
) -> LiquidityState:
    if (
        estimated_runway_years is not None
        and estimated_runway_years >= 3
        and balance_sheet_state is BalanceSheetState.NET_CASH
    ):
        return LiquidityState.VERY_STRONG

    if (
        estimated_runway_years is not None
        and estimated_runway_years >= 2
        and balance_sheet_state is BalanceSheetState.NET_CASH
    ):
        return LiquidityState.STRONG

    if (
        estimated_runway_years is not None
        and estimated_runway_years >= 1
    ):
        return LiquidityState.ADEQUATE

    if free_cash_flow is not None and free_cash_flow < 0:
        return LiquidityState.CONSTRAINED

    return LiquidityState.UNKNOWN


def build_financial_metrics(
    *,
    cash: float | None,
    debt: float | None,
    market_cap: float | None = None,
    enterprise_value: float | None = None,
    free_cash_flow: float | None = None,
    estimated_runway: Any = None,
) -> FinancialMetrics:
    net_position = calculate_net_position(
        cash=cash,
        debt=debt,
    )
    balance_sheet_state = classify_balance_sheet_state(
        net_position
    )
    runway_years = parse_runway_years(
        estimated_runway
    )

    return FinancialMetrics(
        cash=cash,
        debt=debt,
        net_position=net_position,
        balance_sheet_state=balance_sheet_state,
        market_cap=market_cap,
        enterprise_value=enterprise_value,
        enterprise_value_relation=(
            classify_enterprise_value_relation(
                enterprise_value=enterprise_value,
                market_cap=market_cap,
            )
        ),
        estimated_runway_years=runway_years,
        liquidity_state=classify_liquidity_state(
            balance_sheet_state=balance_sheet_state,
            estimated_runway_years=runway_years,
            free_cash_flow=free_cash_flow,
        ),
    )
