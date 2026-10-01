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
from services.reports.reconciliation import validate_report_for_delivery

pytestmark = pytest.mark.integration


def test_provider_fixture_reconciles_without_network(load_fixture):
    fixture = load_fixture("providers/sample_company.json")
    period = date.fromisoformat(fixture["balance_sheet"]["period_end"])

    def metric(name, value, unit="USD"):
        return ValidatedMetric(
            name=name,
            display_name=name.replace("_", " ").title(),
            value=value,
            unit=unit,
            confidence=MetricConfidence.HIGH,
            validation_status=MetricValidationStatus.VERIFIED,
            provenance=MetricProvenance(
                source_type=MetricSourceType.SEC,
                source_name="fixture:sample_company.json",
                period_end=period,
            ),
            period_end=period,
        )

    model = build_financial_render_model(
        {
            "share_price": metric("share_price", fixture["market"]["share_price"]),
            "market_cap": metric("market_cap", fixture["market"]["market_cap"]),
            "cash": metric("cash", fixture["balance_sheet"]["cash"]),
            "financial_debt": metric("financial_debt", fixture["balance_sheet"]["financial_debt"]),
        }
    )
    report = {
        "financial_render_model": model.to_dict(),
        "dashboard_metrics": [
            {"label": "Share Price", "value": "$20.00"},
            {"label": "Market Cap", "value": "$2.00B"},
            {"label": "Cash", "value": "$500.0M"},
            {"label": "Total Debt", "value": "$100.0M"},
        ],
        "valuation": {"metrics": {"market_cap": 2_000_000_000}},
        "executive_summary": {"metrics": {"cash": "$500.0M"}},
        "charts": {"capital_structure": {"metrics": {"cash": 500_000_000, "financial_debt": 100_000_000}}},
    }
    assert validate_report_for_delivery(report) == []
