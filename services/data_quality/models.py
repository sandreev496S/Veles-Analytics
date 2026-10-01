from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any


class PeriodType(str, Enum):
    INSTANT = "instant"
    QUARTER = "quarter"
    ANNUAL = "annual"
    TTM = "ttm"
    CURRENT = "current"
    UNKNOWN = "unknown"


class SourceConfidence(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    PROVIDER = "provider"
    DERIVED = "derived"
    UNKNOWN = "unknown"


class ValidationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True, slots=True)
class MetricSource:
    source_type: str
    source_name: str
    source_url: str | None = None
    accession_number: str | None = None
    form: str | None = None
    taxonomy_concept: str | None = None
    retrieved_at: datetime | None = None
    confidence: SourceConfidence = (
        SourceConfidence.UNKNOWN
    )


@dataclass(frozen=True, slots=True)
class MetricValue:
    metric: str
    value: float | None
    unit: str
    period_type: PeriodType
    period_start: date | None = None
    period_end: date | None = None
    as_of: datetime | None = None
    filing_date: date | None = None
    fiscal_year: int | None = None
    fiscal_period: str | None = None
    definition: str | None = None
    source: MetricSource | None = None
    transformation: str | None = None
    components: tuple[str, ...] = field(
        default_factory=tuple
    )
    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def has_period_reference(self) -> bool:
        return (
            self.period_end is not None
            or self.as_of is not None
        )

    @property
    def has_provenance(self) -> bool:
        return self.source is not None

    def period_label(self) -> str:
        if self.period_end is not None:
            return self.period_end.isoformat()

        if self.as_of is not None:
            return self.as_of.isoformat()

        return "unknown"


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    message: str
    severity: ValidationSeverity
    metrics: tuple[str, ...] = field(
        default_factory=tuple
    )


@dataclass(frozen=True, slots=True)
class ValidationResult:
    issues: tuple[ValidationIssue, ...] = field(
        default_factory=tuple
    )

    @property
    def passed(self) -> bool:
        return not any(
            issue.severity is ValidationSeverity.ERROR
            for issue in self.issues
        )

    @property
    def has_warnings(self) -> bool:
        return any(
            issue.severity is ValidationSeverity.WARNING
            for issue in self.issues
        )

    @property
    def status(self) -> str:
        if not self.passed:
            return "failed"

        if self.has_warnings:
            return "passed_with_disclosed_warnings"

        return "passed"
