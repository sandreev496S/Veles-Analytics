from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class ReconciliationFinding:
    field: str
    expected: Any
    actual: Any
    severity: str
    message: str
    channel: str = "report"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ReportReconciliationError(ValueError):
    """Raised when a report contains contradictory financial values."""


LABEL_TO_METRIC = {
    "Share Price": "share_price",
    "Market Cap": "market_cap",
    "Enterprise Value": "reconciled_enterprise_value",
    "Cash": "cash",
    "Total Debt": "financial_debt",
}

KEY_TO_METRIC = {
    "share_price": "share_price",
    "market_cap": "market_cap",
    "equity_value": "market_cap",
    "enterprise_value": "reconciled_enterprise_value",
    "reconciled_enterprise_value": "reconciled_enterprise_value",
    "cash": "cash",
    "cash_and_cash_equivalents": "cash",
    "financial_debt": "financial_debt",
    "total_debt": "financial_debt",
}


def _mapping(value: Any) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value
    to_dict = getattr(value, "to_dict", None)
    return to_dict() if callable(to_dict) else {}


def _number(value: Any) -> float | None:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    text = str(value or "").replace(",", "").strip()
    match = re.fullmatch(r"\$?(-?\d+(?:\.\d+)?)([KMBT])?%?", text, re.I)
    if not match:
        return None
    number = float(match.group(1))
    scale = {"K": 1e3, "M": 1e6, "B": 1e9, "T": 1e12}.get(
        (match.group(2) or "").upper(), 1.0
    )
    return number * scale


def _canonical_metrics(report: Mapping[str, Any]) -> Mapping[str, Any]:
    model = _mapping(report.get("financial_render_model"))
    metrics = model.get("metrics", {})
    return metrics if isinstance(metrics, Mapping) else {}


def _canonical_metric(canonical: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    metric = canonical.get(key)
    if metric is None and key == "cash":
        metric = canonical.get("cash_and_cash_equivalents")
    if metric is None and key == "financial_debt":
        metric = canonical.get("validated_financial_debt")
    return metric if isinstance(metric, Mapping) else {}


def _compare(
    *,
    findings: list[ReconciliationFinding],
    canonical: Mapping[str, Any],
    metric_key: str,
    field: str,
    actual: Any,
    channel: str,
    tolerance: float,
) -> None:
    metric = _canonical_metric(canonical, metric_key)
    safe = bool(metric.get("is_safe_for_report"))
    if not safe:
        if actual not in {None, "N/A", "", "Unavailable"}:
            findings.append(
                ReconciliationFinding(
                    field,
                    "N/A",
                    actual,
                    "error",
                    "Unsafe canonical metric leaked into a report output.",
                    channel,
                )
            )
        return

    expected_number = _number(metric.get("value"))
    if expected_number is None:
        expected_number = _number(metric.get("display_value"))
    actual_number = _number(actual)
    allowed_difference = max(1.0, abs(expected_number or 0.0) * tolerance)
    if (
        expected_number is None
        or actual_number is None
        or abs(actual_number - expected_number) > allowed_difference
    ):
        findings.append(
            ReconciliationFinding(
                field,
                metric.get("display_value"),
                actual,
                "error",
                "Rendered value does not reconcile to the prepared canonical metric.",
                channel,
            )
        )


def _structured_metric_mappings(value: Any) -> list[tuple[str, Any]]:
    mapping = _mapping(value)
    metrics = mapping.get("metrics", mapping)
    if not isinstance(metrics, Mapping):
        return []
    return [
        (KEY_TO_METRIC[str(key)], metric_value)
        for key, metric_value in metrics.items()
        if str(key) in KEY_TO_METRIC
    ]


def reconcile_report(report: Mapping[str, Any] | Any, *, tolerance: float = 0.005) -> list[ReconciliationFinding]:
    """Reconcile every structured financial output against the render model.

    Narrative prose and raster chart images are intentionally not parsed. Charts can
    participate by exposing a ``metrics`` mapping in their chart manifest.
    """
    report_mapping = _mapping(report)
    canonical = _canonical_metrics(report_mapping)
    findings: list[ReconciliationFinding] = []

    cards = report_mapping.get("dashboard_metrics", []) or []
    for item in cards:
        card = _mapping(item)
        label = str(card.get("label", ""))
        metric_key = LABEL_TO_METRIC.get(label)
        if metric_key:
            _compare(
                findings=findings,
                canonical=canonical,
                metric_key=metric_key,
                field=label,
                actual=card.get("value"),
                channel="dashboard",
                tolerance=tolerance,
            )

    for channel in ("valuation", "executive_summary"):
        for metric_key, actual in _structured_metric_mappings(report_mapping.get(channel, {})):
            _compare(
                findings=findings,
                canonical=canonical,
                metric_key=metric_key,
                field=metric_key,
                actual=actual,
                channel=channel,
                tolerance=tolerance,
            )

    charts = _mapping(report_mapping.get("charts"))
    for chart_name, chart_manifest in charts.items():
        for metric_key, actual in _structured_metric_mappings(chart_manifest):
            _compare(
                findings=findings,
                canonical=canonical,
                metric_key=metric_key,
                field=f"{chart_name}.{metric_key}",
                actual=actual,
                channel="charts",
                tolerance=tolerance,
            )

    return findings


def validate_report_for_delivery(
    report: Mapping[str, Any] | Any,
    *,
    tolerance: float = 0.005,
    raise_on_error: bool = True,
) -> list[ReconciliationFinding]:
    findings = reconcile_report(report, tolerance=tolerance)
    errors = [finding for finding in findings if finding.severity == "error"]
    if errors and raise_on_error:
        summary = "; ".join(
            f"{item.channel}:{item.field} - {item.message} Expected {item.expected!r}, got {item.actual!r}"
            for item in errors
        )
        raise ReportReconciliationError(
            f"Report failed delivery reconciliation with {len(errors)} error(s): {summary}"
        )
    return findings
