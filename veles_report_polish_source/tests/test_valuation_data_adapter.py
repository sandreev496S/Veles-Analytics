import pytest

from services.valuation.data_adapter import (
    adapt_research_dataset,
    parse_numeric,
)


def test_parse_numeric_compact_values():
    assert parse_numeric("$743.29M") == pytest.approx(
        743_290_000
    )
    assert parse_numeric("$1.13B") == pytest.approx(
        1_130_000_000
    )
    assert parse_numeric("18.35M") == pytest.approx(
        18_350_000
    )
    assert parse_numeric("-3.77") == pytest.approx(
        -3.77
    )


def test_adapter_extracts_normalized_research_values():
    research = {
        "ticker": "TEST",
        "financials": {
            "income_statement": [
                ["Metric", "2025-12-31", "2024-12-31"],
                ["Revenue", "$100.00M", "$80.00M"],
            ],
            "balance_sheet": [
                ["Metric", "Latest"],
                ["Cash & Equivalents", "$250.00M"],
                ["Total Debt", "$50.00M"],
            ],
        },
        "market": {
            "tables": {
                "market_snapshot": [
                    ["Metric", "Value"],
                    ["Share Price", "$10.00"],
                    ["Market Cap", "$1.00B"],
                    ["Enterprise Value", "$800.00M"],
                    ["Beta", "1.20"],
                ]
            }
        },
        "metadata": {
            "generated_at": "2026-07-10T12:00:00",
        },
    }

    snapshot = adapt_research_dataset(research)

    assert snapshot.ticker == "TEST"
    assert snapshot.base_year == 2025
    assert snapshot.base_revenue.value == pytest.approx(
        100_000_000
    )
    assert snapshot.cash.value == pytest.approx(
        250_000_000
    )
    assert snapshot.debt.value == pytest.approx(
        50_000_000
    )
    assert snapshot.beta.value == pytest.approx(1.20)
    assert (
        snapshot.diluted_shares_outstanding.value
        == pytest.approx(100_000_000)
    )
    assert (
        snapshot.diluted_shares_outstanding.status
        == "derived"
    )
