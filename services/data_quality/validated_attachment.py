from __future__ import annotations

from typing import Any, MutableMapping

from services.data_quality.validated_financials import (
    build_validated_metric_registry,
)


def attach_validated_metrics(
    research: MutableMapping[str, Any],
) -> MutableMapping[str, Any]:
    """
    Build and attach the canonical validated metric registry.

    The serialized representation is attached so report adapters,
    APIs, caches, and JSON exports do not need to understand Python
    dataclasses or enums.
    """
    registry = build_validated_metric_registry(research)

    research["validated_metrics"] = registry.to_dict()

    research["validation_summary"] = {
        "metric_count": len(registry.metrics),
        "available_count": len(registry.available()),
        "withheld_count": len(registry.withheld()),
        "safe_for_report_count": sum(
            metric.is_safe_for_report
            for metric in registry.values()
        ),
        "withheld_metrics": sorted(
            registry.withheld()
        ),
    }

    return research
