from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ReconciliationStatus(str, Enum):
    PASSED = "passed"
    FAILED = "failed"
    INSUFFICIENT_DATA = "insufficient_data"


@dataclass(frozen=True, slots=True)
class EnterpriseValueReconciliation:
    provider_enterprise_value: float | None
    reconciled_enterprise_value: float | None
    difference: float | None
    difference_pct: float | None
    tolerance: float | None
    status: ReconciliationStatus
    formula: str = (
        "market_cap + debt_used_for_ev "
        "- cash_used_for_ev"
    )


def reconcile_enterprise_value(
    *,
    market_cap: float | None,
    debt_used_for_ev: float | None,
    cash_used_for_ev: float | None,
    provider_enterprise_value: float | None,
    absolute_tolerance: float = 1_000_000,
    relative_tolerance: float = 0.01,
) -> EnterpriseValueReconciliation:
    required = (
        market_cap,
        debt_used_for_ev,
        cash_used_for_ev,
        provider_enterprise_value,
    )

    if any(value is None for value in required):
        return EnterpriseValueReconciliation(
            provider_enterprise_value=(
                provider_enterprise_value
            ),
            reconciled_enterprise_value=None,
            difference=None,
            difference_pct=None,
            tolerance=None,
            status=(
                ReconciliationStatus.INSUFFICIENT_DATA
            ),
        )

    assert market_cap is not None
    assert debt_used_for_ev is not None
    assert cash_used_for_ev is not None
    assert provider_enterprise_value is not None

    reconciled = (
        market_cap
        + debt_used_for_ev
        - cash_used_for_ev
    )
    difference = (
        provider_enterprise_value - reconciled
    )

    denominator = abs(reconciled)

    difference_pct = (
        abs(difference) / denominator
        if denominator
        else None
    )

    tolerance = max(
        absolute_tolerance,
        abs(reconciled) * relative_tolerance,
    )

    status = (
        ReconciliationStatus.PASSED
        if abs(difference) <= tolerance
        else ReconciliationStatus.FAILED
    )

    return EnterpriseValueReconciliation(
        provider_enterprise_value=(
            provider_enterprise_value
        ),
        reconciled_enterprise_value=reconciled,
        difference=difference,
        difference_pct=difference_pct,
        tolerance=tolerance,
        status=status,
    )
