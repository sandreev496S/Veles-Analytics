from __future__ import annotations

import math
from typing import Any


_MISSING_VALUES = {
    "",
    "N/A",
    "NA",
    "None",
    "Unknown",
    "-",
    "—",
}


def parse_money(value: Any) -> float | None:
    """
    Convert formatted financial text into raw numeric units.

    Examples:
        "$1.25B"       -> 1_250_000_000
        "($245.35M)"   -> -245_350_000
        "-$245.35M"    -> -245_350_000
    """

    if value is None or isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        number = float(value)
        return number if math.isfinite(number) else None

    text = str(value).strip()

    if text in _MISSING_VALUES:
        return None

    negative = False

    if text.startswith("(") and text.endswith(")"):
        negative = True
        text = text[1:-1].strip()

    text = (
        text
        .replace("$", "")
        .replace(",", "")
        .replace(" ", "")
    )

    if text.startswith("-"):
        negative = True
        text = text[1:]

    if not text:
        return None

    multiplier = 1.0
    suffix = text[-1:].upper()

    if suffix == "B":
        multiplier = 1_000_000_000
        text = text[:-1]
    elif suffix == "M":
        multiplier = 1_000_000
        text = text[:-1]
    elif suffix == "K":
        multiplier = 1_000
        text = text[:-1]

    try:
        result = float(text) * multiplier
    except (TypeError, ValueError):
        return None

    if not math.isfinite(result):
        return None

    return -abs(result) if negative else result


def _apply_negative_style(
    formatted: str,
    *,
    negative: bool,
    accounting: bool,
) -> str:
    if not negative:
        return formatted

    if accounting:
        return f"({formatted})"

    return f"-{formatted}"


def format_report_money(
    value: float | int | None,
    *,
    accounting: bool = True,
) -> str:
    """
    Format money for report narratives and dashboards.

    Examples:
        1_420_000_000 -> "$1.4B"
        604_790_000   -> "$605M"
        -245_350_000  -> "($245M)"
    """

    if value is None:
        return "N/A"

    try:
        number = float(value)
    except (TypeError, ValueError):
        return "N/A"

    if not math.isfinite(number):
        return "N/A"

    negative = number < 0
    absolute = abs(number)

    if absolute >= 1_000_000_000:
        formatted = (
            f"${absolute / 1_000_000_000:,.1f}B"
        )
    elif absolute >= 1_000_000:
        formatted = (
            f"${absolute / 1_000_000:,.0f}M"
        )
    elif absolute >= 1_000:
        formatted = (
            f"${absolute / 1_000:,.0f}K"
        )
    else:
        formatted = f"${absolute:,.0f}"

    return _apply_negative_style(
        formatted,
        negative=negative,
        accounting=accounting,
    )


def format_precise_money(
    value: float | int | None,
    *,
    accounting: bool = True,
) -> str:
    """
    Format valuation-scale money with two decimals.

    Examples:
        1_420_000_000 -> "$1.42B"
        15_270_000    -> "$15.27M"
        -245_350_000  -> "($245.35M)"
    """

    if value is None:
        return "N/A"

    try:
        number = float(value)
    except (TypeError, ValueError):
        return "N/A"

    if not math.isfinite(number):
        return "N/A"

    negative = number < 0
    absolute = abs(number)

    if absolute >= 1_000_000_000:
        formatted = (
            f"${absolute / 1_000_000_000:,.2f}B"
        )
    elif absolute >= 1_000_000:
        formatted = (
            f"${absolute / 1_000_000:,.2f}M"
        )
    else:
        formatted = f"${absolute:,.2f}"

    return _apply_negative_style(
        formatted,
        negative=negative,
        accounting=accounting,
    )


def format_share_price(
    value: float | int | None,
    *,
    accounting: bool = True,
) -> str:
    """
    Format per-share values without magnitude abbreviations.
    """

    if value is None:
        return "N/A"

    try:
        number = float(value)
    except (TypeError, ValueError):
        return "N/A"

    if not math.isfinite(number):
        return "N/A"

    formatted = f"${abs(number):,.2f}"

    return _apply_negative_style(
        formatted,
        negative=number < 0,
        accounting=accounting,
    )
