from datetime import date

import pandas as pd

from services.providers.yahoo_raw import (
    get_latest_raw_statement_value,
    get_raw_statement_series,
    safe_number,
)


def test_safe_number_preserves_numeric_precision():
    assert safe_number(743_294_000) == 743_294_000.0
    assert safe_number("743294000") == 743_294_000.0
    assert safe_number(None) is None
    assert safe_number(float("nan")) is None


def test_raw_statement_series_preserves_periods():
    frame = pd.DataFrame(
        {
            pd.Timestamp("2025-12-31"): [
                74_256_000,
            ],
            pd.Timestamp("2024-12-31"): [
                58_488_000,
            ],
        },
        index=["Total Revenue"],
    )

    result = get_raw_statement_series(
        frame,
        "Total Revenue",
    )

    assert result == [
        {
            "period_end": "2025-12-31",
            "value": 74_256_000.0,
        },
        {
            "period_end": "2024-12-31",
            "value": 58_488_000.0,
        },
    ]


def test_latest_raw_value_preserves_date():
    frame = pd.DataFrame(
        {
            pd.Timestamp(date(2026, 3, 31)): [
                654_473_000,
            ],
        },
        index=["Cash And Cash Equivalents"],
    )

    result = get_latest_raw_statement_value(
        frame,
        "Cash And Cash Equivalents",
    )

    assert result["period_end"] == "2026-03-31"
    assert result["value"] == 654_473_000.0


def test_missing_row_returns_empty_observation():
    frame = pd.DataFrame()

    result = get_latest_raw_statement_value(
        frame,
        "Total Debt",
    )

    assert result == {
        "period_end": None,
        "value": None,
    }
