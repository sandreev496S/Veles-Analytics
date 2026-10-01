from __future__ import annotations

from typing import Any


PERIODIC_FORMS = {
    "10-K",
    "10-Q",
    "20-F",
    "40-F",
    "6-K",
}


def retain_periodic_facts(
    observations: list[dict[str, Any]],
    *,
    limit: int = 80,
) -> list[dict[str, Any]]:
    """
    Retain enough periodic SEC observations for annual and quarterly
    historical resolution.

    Deduplication remains the responsibility of the downstream SEC
    fact resolver.
    """
    periodic = [
        observation
        for observation in observations
        if str(
            observation.get("form", "")
        ).upper().strip()
        in PERIODIC_FORMS
    ]

    return sorted(
        periodic,
        key=lambda observation: (
            str(observation.get("end", "")),
            str(observation.get("filed", "")),
        ),
        reverse=True,
    )[:limit]
