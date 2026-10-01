from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import date, datetime
from enum import Enum
from typing import Any, Iterable

from services.data_quality.sec_facts import (
    ResolvedSECFact,
)


class MetricConfidence(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    WITHHELD = "withheld"


class MetricValidationStatus(str, Enum):
    VERIFIED = "verified"
    DERIVED = "derived"
    FALLBACK = "fallback"
    PARTIAL = "partial"
    WITHHELD = "withheld"
    UNAVAILABLE = "unavailable"


class MetricSourceType(str, Enum):
    SEC = "sec"
    MARKET_PROVIDER = "market_provider"
    FINANCIAL_PROVIDER = "financial_provider"
    CALCULATED = "calculated"
    COMPANY_DISCLOSURE = "company_disclosure"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class MetricProvenance:
    source_type: MetricSourceType
    source_name: str

    provider: str | None = None
    concept: str | None = None
    taxonomy: str | None = None

    filing_form: str | None = None
    accession_number: str | None = None
    filing_date: date | None = None

    period_start: date | None = None
    period_end: date | None = None
    retrieved_at: datetime | None = None

    definition: str | None = None
    formula: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)

        payload["source_type"] = self.source_type.value

        for field in (
            "filing_date",
            "period_start",
            "period_end",
        ):
            value = payload.get(field)

            if isinstance(value, date):
                payload[field] = value.isoformat()

        retrieved_at = payload.get("retrieved_at")

        if isinstance(retrieved_at, datetime):
            payload["retrieved_at"] = retrieved_at.isoformat()

        return payload


@dataclass(frozen=True, slots=True)
class MetricDependency:
    metric_name: str
    value: float | None
    unit: str | None
    period_end: date | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "value": self.value,
            "unit": self.unit,
            "period_end": (
                self.period_end.isoformat()
                if self.period_end
                else None
            ),
        }


@dataclass(frozen=True, slots=True)
class ValidatedMetric:
    name: str
    display_name: str
    value: float | None
    unit: str

    confidence: MetricConfidence
    validation_status: MetricValidationStatus
    provenance: MetricProvenance

    period_end: date | None = None
    as_of: datetime | None = None

    warnings: tuple[str, ...] = ()
    dependencies: tuple[MetricDependency, ...] = ()

    @property
    def is_available(self) -> bool:
        return self.value is not None

    @property
    def is_withheld(self) -> bool:
        return (
            self.validation_status
            is MetricValidationStatus.WITHHELD
        )

    @property
    def is_safe_for_report(self) -> bool:
        return (
            self.value is not None
            and self.validation_status
            in {
                MetricValidationStatus.VERIFIED,
                MetricValidationStatus.DERIVED,
                MetricValidationStatus.FALLBACK,
            }
        )

    @property
    def provenance_key(self) -> str:
        accession = (
            self.provenance.accession_number
            or "no-accession"
        )
        period = (
            self.period_end.isoformat()
            if self.period_end
            else "no-period"
        )

        return f"{self.name}:{period}:{accession}"

    def with_warning(
        self,
        warning: str,
    ) -> ValidatedMetric:
        return ValidatedMetric(
            name=self.name,
            display_name=self.display_name,
            value=self.value,
            unit=self.unit,
            confidence=self.confidence,
            validation_status=self.validation_status,
            provenance=self.provenance,
            period_end=self.period_end,
            as_of=self.as_of,
            warnings=(
                *self.warnings,
                warning,
            ),
            dependencies=self.dependencies,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "display_name": self.display_name,
            "value": self.value,
            "unit": self.unit,
            "confidence": self.confidence.value,
            "validation_status": (
                self.validation_status.value
            ),
            "period_end": (
                self.period_end.isoformat()
                if self.period_end
                else None
            ),
            "as_of": (
                self.as_of.isoformat()
                if self.as_of
                else None
            ),
            "warnings": list(self.warnings),
            "dependencies": [
                dependency.to_dict()
                for dependency in self.dependencies
            ],
            "provenance": self.provenance.to_dict(),
            "is_available": self.is_available,
            "is_safe_for_report": self.is_safe_for_report,
            "provenance_key": self.provenance_key,
        }


def metric_from_sec_fact(
    *,
    name: str,
    display_name: str,
    fact: ResolvedSECFact,
    confidence: MetricConfidence = MetricConfidence.HIGH,
    warnings: Iterable[str] = (),
) -> ValidatedMetric:
    return ValidatedMetric(
        name=name,
        display_name=display_name,
        value=fact.value,
        unit=fact.unit,
        confidence=confidence,
        validation_status=(
            MetricValidationStatus.VERIFIED
        ),
        period_end=fact.period_end,
        provenance=MetricProvenance(
            source_type=MetricSourceType.SEC,
            source_name=fact.source_name,
            concept=fact.concept,
            taxonomy=fact.concept,
            filing_form=fact.form,
            accession_number=fact.accession_number,
            filing_date=fact.filing_date,
            period_start=fact.period_start,
            period_end=fact.period_end,
        ),
        warnings=tuple(warnings),
    )


def metric_from_provider_value(
    *,
    name: str,
    display_name: str,
    value: float,
    unit: str,
    provider: str,
    source_type: MetricSourceType,
    period_end: date | None = None,
    as_of: datetime | None = None,
    taxonomy: str | None = None,
    definition: str | None = None,
    confidence: MetricConfidence = MetricConfidence.MEDIUM,
    status: MetricValidationStatus = (
        MetricValidationStatus.FALLBACK
    ),
    warnings: Iterable[str] = (),
) -> ValidatedMetric:
    return ValidatedMetric(
        name=name,
        display_name=display_name,
        value=float(value),
        unit=unit,
        confidence=confidence,
        validation_status=status,
        period_end=period_end,
        as_of=as_of,
        provenance=MetricProvenance(
            source_type=source_type,
            source_name=provider,
            provider=provider,
            taxonomy=taxonomy,
            period_end=period_end,
            retrieved_at=as_of,
            definition=definition,
        ),
        warnings=tuple(warnings),
    )


def derived_metric(
    *,
    name: str,
    display_name: str,
    value: float,
    unit: str,
    formula: str,
    dependencies: Iterable[ValidatedMetric],
    period_end: date | None = None,
    as_of: datetime | None = None,
    warnings: Iterable[str] = (),
) -> ValidatedMetric:
    dependency_tuple = tuple(dependencies)

    return ValidatedMetric(
        name=name,
        display_name=display_name,
        value=float(value),
        unit=unit,
        confidence=MetricConfidence.HIGH,
        validation_status=MetricValidationStatus.DERIVED,
        period_end=period_end,
        as_of=as_of,
        provenance=MetricProvenance(
            source_type=MetricSourceType.CALCULATED,
            source_name="Veles Analytics",
            period_end=period_end,
            retrieved_at=as_of,
            formula=formula,
        ),
        warnings=tuple(warnings),
        dependencies=tuple(
            MetricDependency(
                metric_name=metric.name,
                value=metric.value,
                unit=metric.unit,
                period_end=metric.period_end,
            )
            for metric in dependency_tuple
        ),
    )


def withheld_metric(
    *,
    name: str,
    display_name: str,
    unit: str,
    reason: str,
    period_end: date | None = None,
    as_of: datetime | None = None,
    dependencies: Iterable[ValidatedMetric] = (),
) -> ValidatedMetric:
    dependency_tuple = tuple(dependencies)

    return ValidatedMetric(
        name=name,
        display_name=display_name,
        value=None,
        unit=unit,
        confidence=MetricConfidence.WITHHELD,
        validation_status=MetricValidationStatus.WITHHELD,
        period_end=period_end,
        as_of=as_of,
        provenance=MetricProvenance(
            source_type=MetricSourceType.UNAVAILABLE,
            source_name="Veles validation engine",
            period_end=period_end,
            retrieved_at=as_of,
            definition=reason,
        ),
        warnings=(reason,),
        dependencies=tuple(
            MetricDependency(
                metric_name=metric.name,
                value=metric.value,
                unit=metric.unit,
                period_end=metric.period_end,
            )
            for metric in dependency_tuple
        ),
    )


def unavailable_metric(
    *,
    name: str,
    display_name: str,
    unit: str,
    reason: str,
) -> ValidatedMetric:
    return ValidatedMetric(
        name=name,
        display_name=display_name,
        value=None,
        unit=unit,
        confidence=MetricConfidence.WITHHELD,
        validation_status=(
            MetricValidationStatus.UNAVAILABLE
        ),
        provenance=MetricProvenance(
            source_type=MetricSourceType.UNAVAILABLE,
            source_name="Veles validation engine",
            definition=reason,
        ),
        warnings=(reason,),
    )
