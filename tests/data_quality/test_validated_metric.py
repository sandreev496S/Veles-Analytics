from datetime import date, datetime, timezone

from services.data_quality.sec_facts import (
    ResolvedSECFact,
)
from services.data_quality.validated_metric import (
    MetricConfidence,
    MetricValidationStatus,
    derived_metric,
    metric_from_sec_fact,
    withheld_metric,
)


def _sec_fact() -> ResolvedSECFact:
    return ResolvedSECFact(
        concept=(
            "CashAndCashEquivalentsAtCarryingValue"
        ),
        value=654_473_000,
        unit="USD",
        form="10-Q",
        fiscal_year=2026,
        fiscal_period="Q1",
        period_start=None,
        period_end=date(2026, 3, 31),
        filing_date=date(2026, 5, 6),
        accession_number="0001601830-26-000078",
        frame="CY2026Q1I",
    )


def test_metric_from_sec_fact_preserves_provenance():
    metric = metric_from_sec_fact(
        name="cash_and_cash_equivalents",
        display_name="Cash and Cash Equivalents",
        fact=_sec_fact(),
    )

    assert metric.value == 654_473_000
    assert metric.confidence is MetricConfidence.HIGH
    assert (
        metric.validation_status
        is MetricValidationStatus.VERIFIED
    )
    assert metric.period_end == date(2026, 3, 31)
    assert (
        metric.provenance.accession_number
        == "0001601830-26-000078"
    )
    assert metric.is_safe_for_report


def test_derived_metric_records_dependencies():
    cash = metric_from_sec_fact(
        name="cash",
        display_name="Cash",
        fact=_sec_fact(),
    )

    metric = derived_metric(
        name="net_cash",
        display_name="Net Cash",
        value=600_000_000,
        unit="USD",
        formula="cash - debt",
        dependencies=(cash,),
        period_end=date(2026, 3, 31),
        as_of=datetime(
            2026,
            7,
            23,
            tzinfo=timezone.utc,
        ),
    )

    assert (
        metric.validation_status
        is MetricValidationStatus.DERIVED
    )
    assert metric.dependencies[0].metric_name == "cash"
    assert metric.provenance.formula == "cash - debt"
    assert metric.is_safe_for_report


def test_withheld_metric_is_not_report_safe():
    metric = withheld_metric(
        name="enterprise_value",
        display_name="Enterprise Value",
        unit="USD",
        reason="Period-aligned debt was unavailable.",
    )

    assert metric.value is None
    assert metric.is_withheld
    assert not metric.is_safe_for_report
    assert metric.warnings == (
        "Period-aligned debt was unavailable.",
    )


def test_metric_serialization_is_json_ready():
    metric = metric_from_sec_fact(
        name="cash",
        display_name="Cash",
        fact=_sec_fact(),
    )

    payload = metric.to_dict()

    assert payload["value"] == 654_473_000
    assert payload["period_end"] == "2026-03-31"
    assert payload["confidence"] == "high"
    assert (
        payload["provenance"]["filing_date"]
        == "2026-05-06"
    )
