from datetime import date, datetime

from services.data_quality import (
    DebtBreakdown,
    MetricSource,
    MetricValue,
    PeriodType,
    RevenueBreakdown,
    SourceConfidence,
    reconcile_enterprise_value,
    validate_core_report_metrics,
    validate_period_alignment,
)


def _source() -> MetricSource:
    return MetricSource(
        source_type="sec_filing",
        source_name="SEC EDGAR",
        accession_number="0000000000-26-000001",
        form="10-Q",
        taxonomy_concept=(
            "CashAndCashEquivalentsAtCarryingValue"
        ),
        retrieved_at=datetime(2026, 7, 23),
        confidence=SourceConfidence.PRIMARY,
    )


def _metric(
    metric: str,
    value: float,
    period_end: date,
) -> MetricValue:
    return MetricValue(
        metric=metric,
        value=value,
        unit="USD",
        period_type=PeriodType.INSTANT,
        period_end=period_end,
        definition=f"Definition for {metric}",
        source=_source(),
    )


def test_period_alignment_passes_for_same_date():
    result = validate_period_alignment(
        [
            _metric(
                "cash",
                654_473_000,
                date(2026, 3, 31),
            ),
            _metric(
                "debt",
                16_446_000,
                date(2026, 3, 31),
            ),
        ]
    )

    assert result.passed
    assert result.status == "passed"


def test_period_alignment_rejects_mixed_dates():
    result = validate_period_alignment(
        [
            _metric(
                "cash",
                743_294_000,
                date(2025, 12, 31),
            ),
            _metric(
                "debt",
                16_446_000,
                date(2026, 3, 31),
            ),
        ]
    )

    assert not result.passed
    assert result.issues[0].code == "PERIOD_MISMATCH"


def test_debt_taxonomy_separates_operating_leases():
    debt = DebtBreakdown(
        notes_payable=10_000_000,
        finance_lease_current=2_000_000,
        finance_lease_noncurrent=4_000_000,
        operating_lease_current=20_000_000,
        operating_lease_noncurrent=40_000_000,
    )

    assert debt.gross_financial_debt == 16_000_000
    assert (
        debt.operating_lease_liabilities
        == 60_000_000
    )
    assert debt.lease_adjusted_debt == 76_000_000


def test_revenue_taxonomy_distinguishes_total():
    revenue = RevenueBreakdown(
        operating_revenue=74_256_000,
        grant_revenue=425_000,
    )

    assert (
        revenue.computed_total_revenue
        == 74_681_000
    )


def test_enterprise_value_reconciles():
    result = reconcile_enterprise_value(
        market_cap=1_588_000_000,
        debt_used_for_ev=16_446_000,
        cash_used_for_ev=654_473_000,
        provider_enterprise_value=950_000_000,
        absolute_tolerance=2_000_000,
        relative_tolerance=0.01,
    )

    assert result.status.value == "passed"
    assert (
        result.reconciled_enterprise_value
        == 949_973_000
    )


def test_enterprise_value_failure_is_detected():
    result = reconcile_enterprise_value(
        market_cap=1_588_000_000,
        debt_used_for_ev=77_970_000,
        cash_used_for_ev=743_290_000,
        provider_enterprise_value=997_020_000,
        absolute_tolerance=1_000_000,
        relative_tolerance=0.01,
    )

    assert result.status.value == "failed"
    assert abs(result.difference) > 70_000_000


def test_core_validation_fails_closed():
    cash = _metric(
        "cash",
        743_294_000,
        date(2025, 12, 31),
    )
    debt_metric = _metric(
        "debt",
        16_446_000,
        date(2026, 3, 31),
    )

    result = validate_core_report_metrics(
        balance_sheet_metrics=[
            cash,
            debt_metric,
        ],
        report_metrics=[
            cash,
            debt_metric,
        ],
        debt=DebtBreakdown(
            provider_reported_debt=77_970_000,
        ),
        revenue=RevenueBreakdown(
            provider_reported_revenue=74_256_000,
        ),
        market_cap=1_588_000_000,
        cash_used_for_ev=743_290_000,
        debt_used_for_ev=77_970_000,
        provider_enterprise_value=997_020_000,
    )

    codes = {
        issue.code
        for issue in result.issues
    }

    assert not result.passed
    assert "PERIOD_MISMATCH" in codes
    assert "AMBIGUOUS_DEBT_TAXONOMY" in codes
    assert "AMBIGUOUS_REVENUE_TAXONOMY" in codes
    assert "EV_RECONCILIATION_FAILED" in codes
