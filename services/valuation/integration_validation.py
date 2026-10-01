from __future__ import annotations

from typing import Any


class DCFIntegrationError(ValueError):
    pass


REQUIRED_PAYLOAD_PATHS = [
    ("base_result",),
    ("base_result", "forecast"),
    ("base_result", "assumptions"),
    ("scenarios",),
    ("sensitivity",),
    ("assumption_build",),
    ("assumption_build", "assumptions"),
    ("snapshot",),
]


def _get_nested(
    payload: dict[str, Any],
    path: tuple[str, ...],
) -> Any:
    current: Any = payload

    for key in path:
        if not isinstance(current, dict):
            return None

        current = current.get(key)

    return current


def validate_complete_dcf_payload(
    payload: dict[str, Any],
) -> list[str]:
    errors: list[str] = []

    for path in REQUIRED_PAYLOAD_PATHS:
        value = _get_nested(payload, path)

        if (
            value is None
            or value == ""
            or value == []
            or value == {}
        ):
            errors.append(".".join(path))

    base_result = payload.get("base_result", {})
    scenarios = payload.get("scenarios", {})
    sensitivity = payload.get("sensitivity", {})

    if base_result:
        if base_result.get("implied_value_per_share") is None:
            errors.append(
                "base_result.implied_value_per_share"
            )

        if base_result.get("enterprise_value") is None:
            errors.append(
                "base_result.enterprise_value"
            )

        if base_result.get("equity_value") is None:
            errors.append(
                "base_result.equity_value"
            )

        if base_result.get("wacc") is None:
            errors.append("base_result.wacc")

    for scenario_name in ["bull", "base", "bear"]:
        scenario = scenarios.get(scenario_name)

        if not scenario:
            errors.append(
                f"scenarios.{scenario_name}"
            )
            continue

        if scenario.get(
            "implied_value_per_share"
        ) is None:
            errors.append(
                f"scenarios.{scenario_name}."
                "implied_value_per_share"
            )

    if sensitivity:
        if not sensitivity.get("wacc_values"):
            errors.append(
                "sensitivity.wacc_values"
            )

        if not sensitivity.get(
            "terminal_growth_values"
        ):
            errors.append(
                "sensitivity.terminal_growth_values"
            )

        if not sensitivity.get("cells"):
            errors.append("sensitivity.cells")

    if errors:
        raise DCFIntegrationError(
            "Incomplete DCF payload. Missing: "
            + ", ".join(sorted(set(errors)))
        )

    return []
