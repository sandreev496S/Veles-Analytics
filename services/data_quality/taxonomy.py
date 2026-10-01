from __future__ import annotations

from dataclasses import dataclass


def _sum_known(
    *values: float | None,
) -> float | None:
    known = [
        value
        for value in values
        if value is not None
    ]

    if not known:
        return None

    return sum(known)


@dataclass(frozen=True, slots=True)
class DebtBreakdown:
    notes_payable: float | None = None
    current_borrowings: float | None = None
    long_term_borrowings: float | None = None
    finance_lease_current: float | None = None
    finance_lease_noncurrent: float | None = None
    operating_lease_current: float | None = None
    operating_lease_noncurrent: float | None = None
    provider_reported_debt: float | None = None
    provider_definition: str | None = None

    @property
    def gross_financial_debt(
        self,
    ) -> float | None:
        return _sum_known(
            self.notes_payable,
            self.current_borrowings,
            self.long_term_borrowings,
            self.finance_lease_current,
            self.finance_lease_noncurrent,
        )

    @property
    def finance_lease_adjusted_debt(
        self,
    ) -> float | None:
        return self.gross_financial_debt

    @property
    def operating_lease_liabilities(
        self,
    ) -> float | None:
        return _sum_known(
            self.operating_lease_current,
            self.operating_lease_noncurrent,
        )

    @property
    def lease_adjusted_debt(
        self,
    ) -> float | None:
        return _sum_known(
            self.gross_financial_debt,
            self.operating_lease_liabilities,
        )

    @property
    def provider_is_ambiguous(self) -> bool:
        return (
            self.provider_reported_debt is not None
            and not self.provider_definition
        )


@dataclass(frozen=True, slots=True)
class RevenueBreakdown:
    operating_revenue: float | None = None
    collaboration_revenue: float | None = None
    license_revenue: float | None = None
    milestone_revenue: float | None = None
    product_revenue: float | None = None
    grant_revenue: float | None = None
    total_revenue: float | None = None
    provider_reported_revenue: float | None = None
    provider_definition: str | None = None

    @property
    def computed_total_revenue(
        self,
    ) -> float | None:
        if self.total_revenue is not None:
            return self.total_revenue

        components = [
            self.operating_revenue,
            self.grant_revenue,
        ]

        known = [
            value
            for value in components
            if value is not None
        ]

        if not known:
            return None

        return sum(known)

    @property
    def provider_is_ambiguous(self) -> bool:
        return (
            self.provider_reported_revenue
            is not None
            and not self.provider_definition
        )
