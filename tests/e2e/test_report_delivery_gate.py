from datetime import date

import pytest

from services.data_quality.validated_metric import (
    MetricConfidence,
    MetricProvenance,
    MetricSourceType,
    MetricValidationStatus,
    ValidatedMetric,
)
from services.reports.financial_render_models import build_financial_render_model
from services.reports.reconciliation import (
    ReportReconciliationError,
    validate_report_for_delivery,
)

pytestmark = pytest.mark.e2e


def _model():
    metric = ValidatedMetric(
        name="market_cap",
        display_name="Market Cap",
        value=2_000_000_000,
        unit="USD",
        confidence=MetricConfidence.HIGH,
        validation_status=MetricValidationStatus.VERIFIED,
        provenance=MetricProvenance(
            source_type=MetricSourceType.SEC,
            source_name="SEC EDGAR",
            period_end=date(2025, 12, 31),
        ),
        period_end=date(2025, 12, 31),
    )
    return build_financial_render_model({"market_cap": metric}).to_dict()


def test_delivery_gate_fails_closed_on_cross_output_conflict():
    report = {
        "financial_render_model": _model(),
        "dashboard_metrics": [{"label": "Market Cap", "value": "$2.00B"}],
        "valuation": {"metrics": {"market_cap": "$1.00B"}},
    }
    with pytest.raises(ReportReconciliationError, match="valuation:market_cap"):
        validate_report_for_delivery(report)


def test_delivery_gate_blocks_unsafe_metric_leakage():
    model = _model()
    model["metrics"]["market_cap"]["is_safe_for_report"] = False
    model["metrics"]["market_cap"]["display_value"] = "N/A"
    report = {
        "financial_render_model": model,
        "dashboard_metrics": [{"label": "Market Cap", "value": "$2.00B"}],
    }
    with pytest.raises(ReportReconciliationError, match="Unsafe canonical metric"):
        validate_report_for_delivery(report)
