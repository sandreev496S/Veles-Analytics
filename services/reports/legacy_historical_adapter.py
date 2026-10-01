from __future__ import annotations

from typing import Any


_MISSING_VALUES = {
    None,
    "",
    "N/A",
    "—",
    "-",
    "None",
    "Unknown",
}


def latest_statement_value(
    table: list[list[Any]],
    metric_name: str,
    column_index: int = 1,
) -> Any:
    """
    Temporary normalized-table adapter pending ValidatedSeries.

    Do not use this function for canonical point-in-time market or
    balance-sheet metrics.
    """
    if not isinstance(table, list):
        return None

    for row in table:
        if not isinstance(row, list):
            continue

        if not row:
            continue

        if str(row[0]).strip() != metric_name:
            continue

        if len(row) <= column_index:
            return None

        value = row[column_index]

        if value in _MISSING_VALUES:
            return None

        return value

    return None
