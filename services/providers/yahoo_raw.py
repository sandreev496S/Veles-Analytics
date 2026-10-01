from __future__ import annotations

from datetime import date
from typing import Any


def safe_number(value: Any) -> float | None:
    """Convert provider scalars to finite floats without formatting."""
    if value is None:
        return None

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    # NaN is the only normal float unequal to itself.
    if number != number:
        return None

    if number in {float("inf"), float("-inf")}:
        return None

    return number


def period_to_iso(value: Any) -> str | None:
    """Convert pandas timestamps and date-like values to ISO dates."""
    if value is None:
        return None

    try:
        if hasattr(value, "date"):
            parsed = value.date()
            if isinstance(parsed, date):
                return parsed.isoformat()
    except Exception:
        pass

    text = str(value).strip()
    return text or None


def get_raw_statement_series(
    dataframe: Any,
    row_name: str,
    *,
    max_periods: int = 3,
) -> list[dict[str, Any]]:
    """Return numeric statement values with their exact period ends."""
    if (
        dataframe is None
        or getattr(dataframe, "empty", True)
        or row_name not in dataframe.index
    ):
        return []

    observations: list[dict[str, Any]] = []

    try:
        columns = list(dataframe.columns)[:max_periods]

        for column in columns:
            observations.append(
                {
                    "period_end": period_to_iso(column),
                    "value": safe_number(
                        dataframe.loc[row_name, column]
                    ),
                }
            )
    except Exception:
        return []

    return observations


def get_latest_raw_statement_value(
    dataframe: Any,
    row_name: str,
) -> dict[str, Any]:
    """Return the latest numeric observation and its period."""
    observations = get_raw_statement_series(
        dataframe,
        row_name,
        max_periods=1,
    )

    if not observations:
        return {
            "period_end": None,
            "value": None,
        }

    return observations[0]
