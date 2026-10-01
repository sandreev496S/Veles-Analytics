from __future__ import annotations

from services.reports.equity_report_assembler import (
    _get_registry_metric,
    _validated_metric_registry,
    _validated_metric_value,
)
from services.reports.legacy_historical_adapter import (
    latest_statement_value,
)


def test_registry_reads_attached_mapping() -> None:
    research = {
        "validated_metrics": {
            "cash": {
                "value": 500_000_000,
                "validation_status": "validated",
                "is_safe_for_report": True,
            }
        }
    }

    registry = _validated_metric_registry(
        research
    )

    assert (
        registry["cash"]["value"]
        == 500_000_000
    )


def test_safe_metric_returns_numeric_value() -> None:
    metric = {
        "value": 500_000_000,
        "validation_status": "validated",
        "is_safe_for_report": True,
    }

    assert (
        _validated_metric_value(metric)
        == 500_000_000.0
    )


def test_withheld_metric_returns_none() -> None:
    metric = {
        "value": 500_000_000,
        "validation_status": "withheld",
        "is_safe_for_report": False,
    }

    assert (
        _validated_metric_value(metric)
        is None
    )


def test_unavailable_metric_is_not_zero() -> None:
    metric = {
        "value": None,
        "validation_status": "unavailable",
        "is_safe_for_report": False,
    }

    assert (
        _validated_metric_value(metric)
        is None
    )


def test_registry_alias_resolution() -> None:
    registry = {
        "cash_and_cash_equivalents": {
            "value": 125_000_000,
        }
    }

    metric = _get_registry_metric(
        registry,
        "cash",
        "cash_and_cash_equivalents",
    )

    assert metric["value"] == 125_000_000


def test_historical_adapter_reads_latest_column() -> None:
    table = [
        ["Metric", "2025", "2024"],
        ["Revenue", "$100M", "$80M"],
    ]

    assert (
        latest_statement_value(
            table,
            "Revenue",
        )
        == "$100M"
    )


def test_historical_adapter_preserves_missingness() -> None:
    table = [
        ["Metric", "2025"],
        ["Revenue", "N/A"],
    ]

    assert (
        latest_statement_value(
            table,
            "Revenue",
        )
        is None
    )
