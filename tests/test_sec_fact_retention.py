from services.providers.sec_fact_retention import (
    retain_periodic_facts,
)


def test_retains_more_than_five_observations():
    observations = [
        {
            "form": "10-K",
            "end": f"{year}-12-31",
            "filed": f"{year + 1}-02-20",
            "val": year,
        }
        for year in range(2018, 2026)
    ]

    result = retain_periodic_facts(observations)

    assert len(result) == 8
    assert result[0]["end"] == "2025-12-31"
    assert result[-1]["end"] == "2018-12-31"


def test_excludes_nonperiodic_forms():
    observations = [
        {
            "form": "10-Q",
            "end": "2026-03-31",
            "filed": "2026-05-06",
        },
        {
            "form": "8-K",
            "end": "2026-04-01",
            "filed": "2026-04-02",
        },
        {
            "form": "144",
            "end": "2026-04-03",
            "filed": "2026-04-03",
        },
    ]

    result = retain_periodic_facts(observations)

    assert len(result) == 1
    assert result[0]["form"] == "10-Q"


def test_latest_amendment_sorts_first():
    observations = [
        {
            "form": "10-K",
            "end": "2025-12-31",
            "filed": "2026-02-20",
            "val": 1,
        },
        {
            "form": "10-K",
            "end": "2025-12-31",
            "filed": "2026-03-01",
            "val": 2,
        },
    ]

    result = retain_periodic_facts(observations)

    assert result[0]["val"] == 2
