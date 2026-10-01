from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime
from typing import Any, Mapping

UNSAFE_STATUSES = {"withheld", "unavailable", "invalid", "failed", "unsafe", "partial"}


def _enum_text(value: Any) -> str:
    return str(getattr(value, "value", value) or "").strip().lower()


def _iso(value: Any) -> str | None:
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if value in (None, ""):
        return None
    return str(value)


def _read(metric: Any, key: str, default: Any = None) -> Any:
    if isinstance(metric, Mapping):
        return metric.get(key, default)
    return getattr(metric, key, default)


def _provenance(metric: Any) -> Mapping[str, Any]:
    value = _read(metric, "provenance", {})
    if isinstance(value, Mapping):
        return value
    to_dict = getattr(value, "to_dict", None)
    return to_dict() if callable(to_dict) else {}


@dataclass(frozen=True, slots=True)
class RenderMetric:
    key: str
    label: str
    value: float | None
    unit: str | None
    display_value: str
    period_end: str | None
    as_of: str | None
    validation_status: str
    confidence: str
    is_safe_for_report: bool
    source_name: str | None
    source_type: str | None
    filing_form: str | None = None
    accession_number: str | None = None
    warnings: tuple[str, ...] = ()
    suppression_reason: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["warnings"] = list(self.warnings)
        return payload


@dataclass(frozen=True, slots=True)
class PeriodConsistencyIssue:
    metric_keys: tuple[str, ...]
    severity: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric_keys": list(self.metric_keys),
            "severity": self.severity,
            "message": self.message,
        }


@dataclass(frozen=True, slots=True)
class FinancialRenderModel:
    metrics: Mapping[str, RenderMetric]
    period_issues: tuple[PeriodConsistencyIssue, ...] = ()
    suppressed_metrics: tuple[str, ...] = ()
    generated_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def safe_metric(self, key: str) -> RenderMetric | None:
        metric = self.metrics.get(key)
        return metric if metric and metric.is_safe_for_report else None

    def to_dict(self) -> dict[str, Any]:
        return {
            "metrics": {key: value.to_dict() for key, value in self.metrics.items()},
            "period_issues": [issue.to_dict() for issue in self.period_issues],
            "suppressed_metrics": list(self.suppressed_metrics),
            "generated_at": self.generated_at,
        }


def _format_value(value: float | None, unit: str | None) -> str:
    if value is None:
        return "N/A"
    normalized = (unit or "").lower()
    if normalized in {"usd", "$"}:
        magnitude = abs(value)
        if magnitude >= 1_000_000_000:
            return f"${value / 1_000_000_000:,.2f}B"
        if magnitude >= 1_000_000:
            return f"${value / 1_000_000:,.1f}M"
        return f"${value:,.2f}"
    if normalized in {"percent", "%"}:
        return f"{value:,.1f}%"
    return f"{value:,.2f}"


def prepare_render_metric(key: str, metric: Any) -> RenderMetric:
    provenance = _provenance(metric)
    value = _read(metric, "value")
    status = _enum_text(_read(metric, "validation_status", _read(metric, "status")))
    explicit_safe = _read(metric, "is_safe_for_report")
    numeric = float(value) if isinstance(value, (int, float)) and not isinstance(value, bool) else None
    safe = bool(numeric is not None and explicit_safe is not False and status not in UNSAFE_STATUSES)
    warnings = tuple(str(item) for item in (_read(metric, "warnings", ()) or ()))
    reason = None
    if not safe:
        if numeric is None:
            reason = "Metric has no resolved numeric value."
        elif explicit_safe is False:
            reason = "Validation layer marked the metric unsafe for reporting."
        elif status in UNSAFE_STATUSES:
            reason = f"Validation status is {status}."
        else:
            reason = "Metric did not satisfy report-safety requirements."

    return RenderMetric(
        key=key,
        label=str(_read(metric, "display_name", key.replace("_", " ").title())),
        value=numeric if safe else None,
        unit=_read(metric, "unit"),
        display_value=_format_value(numeric, _read(metric, "unit")) if safe else "N/A",
        period_end=_iso(_read(metric, "period_end") or provenance.get("period_end")),
        as_of=_iso(_read(metric, "as_of")),
        validation_status=status or "unknown",
        confidence=_enum_text(_read(metric, "confidence")) or "unknown",
        is_safe_for_report=safe,
        source_name=provenance.get("source_name") or provenance.get("provider"),
        source_type=_enum_text(provenance.get("source_type")) or None,
        filing_form=provenance.get("filing_form"),
        accession_number=provenance.get("accession_number"),
        warnings=warnings,
        suppression_reason=reason,
    )


def check_period_consistency(metrics: Mapping[str, RenderMetric], *, max_lag_days: int = 120) -> tuple[PeriodConsistencyIssue, ...]:
    groups = (
        ("cash", "financial_debt", "equity"),
        ("market_cap", "share_price", "reconciled_enterprise_value"),
    )
    issues: list[PeriodConsistencyIssue] = []
    for keys in groups:
        dated: list[tuple[str, date]] = []
        for key in keys:
            metric = metrics.get(key)
            if not metric or not metric.is_safe_for_report or not metric.period_end:
                continue
            try:
                dated.append((key, date.fromisoformat(metric.period_end[:10])))
            except ValueError:
                issues.append(PeriodConsistencyIssue((key,), "warning", f"{key} has an invalid period_end value."))
        if len(dated) >= 2:
            oldest = min(item[1] for item in dated)
            newest = max(item[1] for item in dated)
            lag = (newest - oldest).days
            if lag > max_lag_days:
                issues.append(PeriodConsistencyIssue(tuple(item[0] for item in dated), "error", f"Compared metrics span {lag} days, exceeding the {max_lag_days}-day consistency limit."))
    return tuple(issues)


def build_financial_render_model(registry: Any) -> FinancialRenderModel:
    metrics_source = getattr(registry, "metrics", registry)
    if not isinstance(metrics_source, Mapping):
        metrics_source = {}
    prepared = {str(key): prepare_render_metric(str(key), metric) for key, metric in metrics_source.items()}
    issues = check_period_consistency(prepared)
    unsafe_period_keys = {key for issue in issues if issue.severity == "error" for key in issue.metric_keys}
    if unsafe_period_keys:
        prepared = {
            key: (RenderMetric(**{**metric.to_dict(), "warnings": tuple(metric.warnings) + ("Suppressed because related metrics use inconsistent periods.",), "value": None, "display_value": "N/A", "is_safe_for_report": False, "suppression_reason": "Related financial metrics are not period-consistent."}) if key in unsafe_period_keys else metric)
            for key, metric in prepared.items()
        }
    suppressed = tuple(sorted(key for key, metric in prepared.items() if not metric.is_safe_for_report))
    return FinancialRenderModel(metrics=prepared, period_issues=issues, suppressed_metrics=suppressed)


def provenance_summary(model: FinancialRenderModel) -> str:
    rows = []
    for metric in model.metrics.values():
        if not metric.is_safe_for_report:
            continue
        period = metric.period_end or metric.as_of or "date unavailable"
        source = metric.source_name or "source unavailable"
        status = metric.validation_status
        rows.append(f"{metric.label}: {source}; period/as of {period}; status {status}.")
    return " ".join(rows) if rows else "No report-safe canonical financial metrics were available for provenance disclosure."
