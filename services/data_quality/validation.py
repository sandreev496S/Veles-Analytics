from __future__ import annotations

from collections.abc import Iterable

from services.data_quality.models import (
    MetricValue,
    ValidationIssue,
    ValidationResult,
    ValidationSeverity,
)
from services.data_quality.reconciliation import (
    ReconciliationStatus,
    reconcile_enterprise_value,
)
from services.data_quality.taxonomy import (
    DebtBreakdown,
    RevenueBreakdown,
)


def validate_period_alignment(
    metrics: Iterable[MetricValue],
    *,
    require_period: bool = True,
) -> ValidationResult:
    values = tuple(metrics)
    issues: list[ValidationIssue] = []

    if require_period:
        missing = tuple(
            metric.metric
            for metric in values
            if not metric.has_period_reference
        )

        if missing:
            issues.append(
                ValidationIssue(
                    code="MISSING_PERIOD_REFERENCE",
                    message=(
                        "One or more metrics have no "
                        "period end or as-of timestamp."
                    ),
                    severity=ValidationSeverity.ERROR,
                    metrics=missing,
                )
            )

    period_ends = {
        metric.period_end
        for metric in values
        if metric.period_end is not None
    }

    if len(period_ends) > 1:
        labels = ", ".join(
            sorted(
                period.isoformat()
                for period in period_ends
            )
        )
        issues.append(
            ValidationIssue(
                code="PERIOD_MISMATCH",
                message=(
                    "Metrics use incompatible period "
                    f"ends: {labels}."
                ),
                severity=ValidationSeverity.ERROR,
                metrics=tuple(
                    metric.metric
                    for metric in values
                ),
            )
        )

    return ValidationResult(
        issues=tuple(issues)
    )


def validate_provenance(
    metrics: Iterable[MetricValue],
) -> ValidationResult:
    values = tuple(metrics)
    issues: list[ValidationIssue] = []

    missing_source = tuple(
        metric.metric
        for metric in values
        if metric.source is None
    )

    if missing_source:
        issues.append(
            ValidationIssue(
                code="MISSING_PROVENANCE",
                message=(
                    "One or more report metrics have "
                    "no traceable source."
                ),
                severity=ValidationSeverity.ERROR,
                metrics=missing_source,
            )
        )

    missing_definition = tuple(
        metric.metric
        for metric in values
        if not metric.definition
    )

    if missing_definition:
        issues.append(
            ValidationIssue(
                code="MISSING_METRIC_DEFINITION",
                message=(
                    "One or more report metrics have "
                    "no explicit accounting definition."
                ),
                severity=ValidationSeverity.ERROR,
                metrics=missing_definition,
            )
        )

    return ValidationResult(
        issues=tuple(issues)
    )


def validate_core_report_metrics(
    *,
    balance_sheet_metrics: Iterable[MetricValue],
    report_metrics: Iterable[MetricValue],
    debt: DebtBreakdown,
    revenue: RevenueBreakdown,
    market_cap: float | None = None,
    cash_used_for_ev: float | None = None,
    debt_used_for_ev: float | None = None,
    provider_enterprise_value: float | None = None,
) -> ValidationResult:
    issues: list[ValidationIssue] = []

    period_result = validate_period_alignment(
        balance_sheet_metrics
    )
    issues.extend(period_result.issues)

    provenance_result = validate_provenance(
        report_metrics
    )
    issues.extend(provenance_result.issues)

    if debt.provider_is_ambiguous:
        issues.append(
            ValidationIssue(
                code="AMBIGUOUS_DEBT_TAXONOMY",
                message=(
                    "Provider-reported debt has no "
                    "definition describing whether it "
                    "includes leases or other liabilities."
                ),
                severity=ValidationSeverity.ERROR,
                metrics=("provider_reported_debt",),
            )
        )

    if revenue.provider_is_ambiguous:
        issues.append(
            ValidationIssue(
                code="AMBIGUOUS_REVENUE_TAXONOMY",
                message=(
                    "Provider-reported revenue has no "
                    "definition distinguishing operating "
                    "revenue from total revenue."
                ),
                severity=ValidationSeverity.ERROR,
                metrics=("provider_reported_revenue",),
            )
        )

    ev_result = reconcile_enterprise_value(
        market_cap=market_cap,
        debt_used_for_ev=debt_used_for_ev,
        cash_used_for_ev=cash_used_for_ev,
        provider_enterprise_value=(
            provider_enterprise_value
        ),
    )

    if (
        ev_result.status
        is ReconciliationStatus.FAILED
    ):
        issues.append(
            ValidationIssue(
                code="EV_RECONCILIATION_FAILED",
                message=(
                    "Provider enterprise value does not "
                    "reconcile to the displayed market "
                    "capitalization, debt, and cash inputs."
                ),
                severity=ValidationSeverity.ERROR,
                metrics=(
                    "market_cap",
                    "debt_used_for_ev",
                    "cash_used_for_ev",
                    "provider_enterprise_value",
                ),
            )
        )
    elif (
        ev_result.status
        is ReconciliationStatus.INSUFFICIENT_DATA
    ):
        issues.append(
            ValidationIssue(
                code="EV_RECONCILIATION_UNAVAILABLE",
                message=(
                    "Enterprise value could not be "
                    "reconciled because one or more "
                    "required inputs are missing."
                ),
                severity=ValidationSeverity.WARNING,
                metrics=(
                    "market_cap",
                    "debt_used_for_ev",
                    "cash_used_for_ev",
                    "provider_enterprise_value",
                ),
            )
        )

    return ValidationResult(
        issues=tuple(issues)
    )
