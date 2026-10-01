from services.data_quality.sec_facts import (
    SECPeriodKind,
    select_sec_fact,
    select_sec_series,
)


def test_select_latest_instant_fact():
    facts = {
        "CashAndCashEquivalentsAtCarryingValue": [
            {
                "fy": 2025,
                "fp": "FY",
                "form": "10-K",
                "filed": "2026-02-25",
                "end": "2025-12-31",
                "value": 743_294_000,
                "accession_number": (
                    "0001601830-26-000039"
                ),
            },
            {
                "fy": 2026,
                "fp": "Q1",
                "form": "10-Q",
                "filed": "2026-05-06",
                "end": "2026-03-31",
                "value": 654_473_000,
                "accession_number": (
                    "0001601830-26-000078"
                ),
            },
        ]
    }

    result = select_sec_fact(
        facts,
        concepts=(
            "CashAndCashEquivalentsAtCarryingValue",
        ),
        period_kind=SECPeriodKind.INSTANT,
    )

    assert result is not None
    assert result.value == 654_473_000
    assert result.period_end.isoformat() == "2026-03-31"
    assert result.form == "10-Q"


def test_select_latest_annual_fact():
    facts = {
        "NetIncomeLoss": [
            {
                "fy": 2025,
                "fp": "FY",
                "form": "10-K",
                "filed": "2026-02-25",
                "start": "2025-01-01",
                "end": "2025-12-31",
                "value": -644_759_000,
            },
            {
                "fy": 2026,
                "fp": "Q1",
                "form": "10-Q",
                "filed": "2026-05-06",
                "start": "2026-01-01",
                "end": "2026-03-31",
                "value": -117_504_000,
            },
        ]
    }

    result = select_sec_fact(
        facts,
        concepts=("NetIncomeLoss",),
        period_kind=SECPeriodKind.ANNUAL,
    )

    assert result is not None
    assert result.value == -644_759_000
    assert result.fiscal_period == "FY"


def test_select_latest_quarter_fact():
    facts = {
        "NetIncomeLoss": [
            {
                "fy": 2025,
                "fp": "FY",
                "form": "10-K",
                "filed": "2026-02-25",
                "start": "2025-01-01",
                "end": "2025-12-31",
                "value": -644_759_000,
            },
            {
                "fy": 2026,
                "fp": "Q1",
                "form": "10-Q",
                "filed": "2026-05-06",
                "start": "2026-01-01",
                "end": "2026-03-31",
                "value": -117_504_000,
            },
        ]
    }

    result = select_sec_fact(
        facts,
        concepts=("NetIncomeLoss",),
        period_kind=SECPeriodKind.QUARTER,
    )

    assert result is not None
    assert result.value == -117_504_000
    assert result.fiscal_period == "Q1"


def test_concept_preference_order_is_respected():
    facts = {
        "Revenues": [
            {
                "fy": 2025,
                "fp": "FY",
                "form": "10-K",
                "filed": "2026-02-25",
                "start": "2025-01-01",
                "end": "2025-12-31",
                "value": 74_681_000,
            }
        ],
        "RevenueFromContractWithCustomerExcludingAssessedTax": [
            {
                "fy": 2025,
                "fp": "FY",
                "form": "10-K",
                "filed": "2026-02-25",
                "start": "2025-01-01",
                "end": "2025-12-31",
                "value": 74_256_000,
            }
        ],
    }

    result = select_sec_fact(
        facts,
        concepts=(
            "Revenues",
            "RevenueFromContractWithCustomerExcludingAssessedTax",
        ),
        period_kind=SECPeriodKind.ANNUAL,
    )

    assert result is not None
    assert result.concept == "Revenues"
    assert result.value == 74_681_000


def test_annual_series_is_sorted_and_limited():
    facts = {
        "ResearchAndDevelopmentExpense": [
            {
                "fy": 2023,
                "fp": "FY",
                "form": "10-K",
                "filed": "2024-02-20",
                "end": "2023-12-31",
                "value": 241_226_000,
            },
            {
                "fy": 2025,
                "fp": "FY",
                "form": "10-K",
                "filed": "2026-02-25",
                "end": "2025-12-31",
                "value": 475_271_000,
            },
            {
                "fy": 2024,
                "fp": "FY",
                "form": "10-K",
                "filed": "2025-02-24",
                "end": "2024-12-31",
                "value": 314_421_000,
            },
        ]
    }

    result = select_sec_series(
        facts,
        concepts=(
            "ResearchAndDevelopmentExpense",
        ),
        period_kind=SECPeriodKind.ANNUAL,
        max_periods=2,
    )

    assert [
        item.value
        for item in result
    ] == [
        475_271_000,
        314_421_000,
    ]


def test_missing_concept_returns_none():
    result = select_sec_fact(
        {},
        concepts=("MissingConcept",),
        period_kind=SECPeriodKind.INSTANT,
    )

    assert result is None
