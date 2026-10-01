from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any

from services.data_quality.sec_facts import (
    ResolvedSECFact,
    SECPeriodKind,
    select_sec_fact,
)
from services.data_quality.sec_metric_policy import (
    SEC_CONCEPT_POLICY,
)


@dataclass(frozen=True, slots=True)
class CanonicalBalanceSheet:
    period_end: date
    cash_and_cash_equivalents: ResolvedSECFact
    cash_including_restricted_cash: (
        ResolvedSECFact | None
    )
    stockholders_equity: ResolvedSECFact | None

    short_term_borrowings: ResolvedSECFact | None
    current_financial_debt: ResolvedSECFact | None
    noncurrent_financial_debt: ResolvedSECFact | None
    total_financial_debt: ResolvedSECFact | None

    finance_lease_current: ResolvedSECFact | None
    finance_lease_noncurrent: ResolvedSECFact | None

    operating_lease_current: ResolvedSECFact | None
    operating_lease_noncurrent: ResolvedSECFact | None

    @property
    def resolved_financial_debt_components(
        self,
    ) -> tuple[ResolvedSECFact, ...]:
        return tuple(
            fact
            for fact in (
                self.short_term_borrowings,
                self.current_financial_debt,
                self.noncurrent_financial_debt,
                self.finance_lease_current,
                self.finance_lease_noncurrent,
            )
            if fact is not None
        )

    @property
    def gross_financial_debt(
        self,
    ) -> float | None:
        """
        Return debt only when a complete, explicitly usable debt
        presentation exists.

        A single total-debt fact takes precedence. Otherwise, component
        debt is available only when at least one period-aligned component
        exists. Missing components are not automatically assumed to be
        zero.
        """
        if self.total_financial_debt is not None:
            return self.total_financial_debt.value

        components = self.resolved_financial_debt_components

        if not components:
            return None

        return sum(
            fact.value
            for fact in components
        )

    @property
    def operating_lease_liabilities(
        self,
    ) -> float | None:
        components = (
            self.operating_lease_current,
            self.operating_lease_noncurrent,
        )

        if any(fact is None for fact in components):
            return None

        return sum(
            fact.value
            for fact in components
            if fact is not None
        )

    @property
    def financial_debt_available(
        self,
    ) -> bool:
        return self.gross_financial_debt is not None

    @property
    def debt_resolution_status(self) -> str:
        """
        Describe whether financial debt is fully resolved for the
        selected balance-sheet date.
        """
        if self.total_financial_debt is not None:
            return "resolved_from_total"

        components = self.resolved_financial_debt_components

        if not components:
            return "unresolved"

        return "partially_resolved_from_components"

    @property
    def debt_is_safe_for_ev(self) -> bool:
        """
        Permit EV reconciliation only when an explicit total debt fact
        is available for the exact balance-sheet date.
        """
        return (
            self.debt_resolution_status
            == "resolved_from_total"
        )


def _resolve_exact(
    facts: dict[str, Any],
    metric: str,
    period_end: date,
) -> ResolvedSECFact | None:
    return select_sec_fact(
        facts,
        concepts=SEC_CONCEPT_POLICY[metric],
        period_kind=SECPeriodKind.INSTANT,
        target_period_end=period_end,
    )


def resolve_latest_balance_sheet(
    facts: dict[str, Any],
) -> CanonicalBalanceSheet | None:
    """
    Anchor the entire balance sheet to the latest SEC cash period.

    No older fact is substituted for a missing current-period metric.
    """
    latest_cash = select_sec_fact(
        facts,
        concepts=SEC_CONCEPT_POLICY[
            "cash_and_cash_equivalents"
        ],
        period_kind=SECPeriodKind.INSTANT,
    )

    if latest_cash is None:
        return None

    period_end = latest_cash.period_end

    return CanonicalBalanceSheet(
        period_end=period_end,
        cash_and_cash_equivalents=latest_cash,
        cash_including_restricted_cash=_resolve_exact(
            facts,
            "cash_including_restricted_cash",
            period_end,
        ),
        stockholders_equity=_resolve_exact(
            facts,
            "stockholders_equity",
            period_end,
        ),
        short_term_borrowings=_resolve_exact(
            facts,
            "short_term_borrowings",
            period_end,
        ),
        current_financial_debt=_resolve_exact(
            facts,
            "current_financial_debt",
            period_end,
        ),
        noncurrent_financial_debt=_resolve_exact(
            facts,
            "noncurrent_financial_debt",
            period_end,
        ),
        total_financial_debt=_resolve_exact(
            facts,
            "total_financial_debt",
            period_end,
        ),
        finance_lease_current=_resolve_exact(
            facts,
            "finance_lease_current",
            period_end,
        ),
        finance_lease_noncurrent=_resolve_exact(
            facts,
            "finance_lease_noncurrent",
            period_end,
        ),
        operating_lease_current=_resolve_exact(
            facts,
            "operating_lease_current",
            period_end,
        ),
        operating_lease_noncurrent=_resolve_exact(
            facts,
            "operating_lease_noncurrent",
            period_end,
        ),
    )
