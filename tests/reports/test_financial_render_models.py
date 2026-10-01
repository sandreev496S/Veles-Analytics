from datetime import date

from services.data_quality.validated_metric import (
    MetricConfidence, MetricProvenance, MetricSourceType,
    MetricValidationStatus, ValidatedMetric,
)
from services.reports.financial_render_models import build_financial_render_model
from services.reports.reconciliation import reconcile_report


def metric(name, value, period, status=MetricValidationStatus.VERIFIED):
    return ValidatedMetric(
        name=name, display_name=name.replace('_', ' ').title(), value=value,
        unit='USD', confidence=MetricConfidence.HIGH,
        validation_status=status,
        provenance=MetricProvenance(source_type=MetricSourceType.SEC, source_name='SEC EDGAR', period_end=period),
        period_end=period,
    )


def test_unsafe_metric_is_suppressed():
    model = build_financial_render_model({'cash': metric('cash', 100, date(2025, 12, 31), MetricValidationStatus.WITHHELD)})
    assert model.metrics['cash'].display_value == 'N/A'
    assert not model.metrics['cash'].is_safe_for_report
    assert 'cash' in model.suppressed_metrics


def test_period_mismatch_suppresses_related_balance_sheet_metrics():
    model = build_financial_render_model({
        'cash': metric('cash', 100, date(2025, 12, 31)),
        'financial_debt': metric('financial_debt', 40, date(2024, 6, 30)),
    })
    assert model.period_issues
    assert not model.metrics['cash'].is_safe_for_report
    assert not model.metrics['financial_debt'].is_safe_for_report


def test_reconciliation_accepts_prepared_dashboard_values():
    model = build_financial_render_model({'market_cap': metric('market_cap', 2_000_000_000, date(2025, 12, 31))})
    report = {'financial_render_model': model.to_dict(), 'dashboard_metrics': [{'label': 'Market Cap', 'value': '$2.00B'}]}
    assert reconcile_report(report) == []


def test_reconciliation_detects_conflict():
    model = build_financial_render_model({'market_cap': metric('market_cap', 2_000_000_000, date(2025, 12, 31))})
    report = {'financial_render_model': model.to_dict(), 'dashboard_metrics': [{'label': 'Market Cap', 'value': '$1.00B'}]}
    assert reconcile_report(report)
