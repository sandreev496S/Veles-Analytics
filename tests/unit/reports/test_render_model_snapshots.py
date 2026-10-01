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

pytestmark = pytest.mark.unit


def _metric(name: str, value: float) -> ValidatedMetric:
    return ValidatedMetric(
        name=name,
        display_name=name.replace("_", " ").title(),
        value=value,
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


def test_financial_render_model_contract_snapshot(assert_json_snapshot):
    model = build_financial_render_model(
        {
            "cash": _metric("cash", 500_000_000),
            "financial_debt": _metric("financial_debt", 100_000_000),
        }
    ).to_dict()
    model.pop("generated_at")
    assert_json_snapshot("financial_render_model_contract.json", model)
