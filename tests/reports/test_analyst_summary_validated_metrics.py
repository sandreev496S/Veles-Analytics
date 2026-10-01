from __future__ import annotations

from dataclasses import dataclass

from services.reports.analyst_summary import (
    _numeric_statement_series,
    _validated_metric_value,
)


@dataclass
class FakeMetric:
    value: float | None
    is_safe_for_report: bool
    validation_status: str


@dataclass
class FakeRegistry:
    metrics: dict[str, FakeMetric]


def test_reads_safe_metric_from_registry_object() -> None:
    registry = FakeRegistry(
        metrics={
            "cash_and_cash_equivalents": FakeMetric(
                value=425_000_000,
                is_safe_for_report=True,
                validation_status="verified",
            )
        }
    )

    assert (
        _validated_metric_value(
            registry,
            "cash_and_cash_equivalents",
        )
        == 425_000_000.0
    )


def test_withheld_metric_is_not_reported() -> None:
    registry = FakeRegistry(
        metrics={
            "financial_debt": FakeMetric(
                value=50_000_000,
                is_safe_for_report=False,
                validation_status="withheld",
            )
        }
    )

    assert (
        _validated_metric_value(
            registry,
            "financial_debt",
        )
        is None
    )


def test_partial_metric_is_not_reported() -> None:
    registry = {
        "financial_debt": {
            "value": 50_000_000,
            "is_safe_for_report": False,
            "validation_status": "partial",
        }
    }

    assert (
        _validated_metric_value(
            registry,
            "financial_debt",
        )
        is None
    )


def test_missing_metric_is_not_zero() -> None:
    assert (
        _validated_metric_value(
            {},
            "cash_and_cash_equivalents",
        )
        is None
    )


def test_numeric_historical_series_is_preserved() -> None:
    table = [
        ["Metric", "2025", "2024"],
        ["Revenue", 125_000_000, 100_000_000],
    ]

    assert _numeric_statement_series(
        table,
        "Revenue",
    ) == [
        125_000_000.0,
        100_000_000.0,
    ]


def test_formatted_historical_strings_are_not_reparsed() -> None:
    table = [
        ["Metric", "2025", "2024"],
        ["Revenue", "$125M", "$100M"],
    ]

    assert (
        _numeric_statement_series(
            table,
            "Revenue",
        )
        == []
    )
