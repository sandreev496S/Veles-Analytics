from services.data_quality.validated_financials import (
    build_validated_metric_registry,
)


def _research_dataset() -> dict:
    return {
        "market": {
            "as_of": "2026-07-23T22:27:45+00:00",
            "raw_metrics": {
                "share_price": {
                    "value": 3.01,
                    "unit": "USD",
                },
                "market_cap": {
                    "value": 1_597_594_240,
                    "unit": "USD",
                    "definition": (
                        "Provider-reported equity "
                        "market capitalization."
                    ),
                },
                "provider_enterprise_value": {
                    "value": 997_019_520,
                    "unit": "USD",
                },
            },
        },
        "sec": {
            "company_facts": {
                "facts": {
                    (
                        "CashAndCashEquivalentsAt"
                        "CarryingValue"
                    ): [
                        {
                            "fy": 2026,
                            "fp": "Q1",
                            "form": "10-Q",
                            "filed": "2026-05-06",
                            "end": "2026-03-31",
                            "frame": "CY2026Q1I",
                            "accession_number": (
                                "0001601830-26-000078"
                            ),
                            "value": 654_473_000,
                        }
                    ],
                    (
                        "CashCashEquivalents"
                        "RestrictedCashAndRestricted"
                        "CashEquivalents"
                    ): [
                        {
                            "fy": 2026,
                            "fp": "Q1",
                            "form": "10-Q",
                            "filed": "2026-05-06",
                            "end": "2026-03-31",
                            "accession_number": (
                                "0001601830-26-000078"
                            ),
                            "value": 665_180_000,
                        }
                    ],
                    "StockholdersEquity": [
                        {
                            "fy": 2026,
                            "fp": "Q1",
                            "form": "10-Q",
                            "filed": "2026-05-06",
                            "end": "2026-03-31",
                            "accession_number": (
                                "0001601830-26-000078"
                            ),
                            "value": 1_024_769_000,
                        }
                    ],
                    "OperatingLeaseLiabilityCurrent": [
                        {
                            "fy": 2026,
                            "fp": "Q1",
                            "form": "10-Q",
                            "filed": "2026-05-06",
                            "end": "2026-03-31",
                            "accession_number": (
                                "0001601830-26-000078"
                            ),
                            "value": 13_087_000,
                        }
                    ],
                    (
                        "OperatingLeaseLiability"
                        "Noncurrent"
                    ): [
                        {
                            "fy": 2026,
                            "fp": "Q1",
                            "form": "10-Q",
                            "filed": "2026-05-06",
                            "end": "2026-03-31",
                            "accession_number": (
                                "0001601830-26-000078"
                            ),
                            "value": 42_842_000,
                        }
                    ],
                }
            }
        },
    }


def test_registry_uses_sec_for_balance_sheet():
    registry = build_validated_metric_registry(
        _research_dataset()
    )

    cash = registry["cash_and_cash_equivalents"]

    assert cash.value == 654_473_000
    assert cash.provenance.source_type.value == "sec"
    assert cash.period_end.isoformat() == "2026-03-31"


def test_registry_uses_market_provider_for_market_cap():
    registry = build_validated_metric_registry(
        _research_dataset()
    )

    market_cap = registry["market_cap"]

    assert market_cap.value == 1_597_594_240
    assert (
        market_cap.provenance.source_type.value
        == "market_provider"
    )


def test_registry_derives_operating_leases():
    registry = build_validated_metric_registry(
        _research_dataset()
    )

    leases = registry[
        "operating_lease_liabilities"
    ]

    assert leases.value == 55_929_000
    assert (
        leases.validation_status.value
        == "derived"
    )
    assert len(leases.dependencies) == 2


def test_registry_withholds_unreconciled_ev():
    registry = build_validated_metric_registry(
        _research_dataset()
    )

    debt = registry["financial_debt"]
    ev = registry[
        "reconciled_enterprise_value"
    ]

    assert debt.value is None
    assert debt.validation_status.value == "withheld"

    assert ev.value is None
    assert ev.validation_status.value == "withheld"
    assert not ev.is_safe_for_report
    assert ev.as_of is not None
    assert (
        ev.as_of.isoformat()
        == "2026-07-23T22:27:45+00:00"
    )
    assert ev.as_of is not None
    assert (
        ev.as_of.isoformat()
        == "2026-07-23T22:27:45+00:00"
    )


def test_registry_serializes_all_metrics():
    registry = build_validated_metric_registry(
        _research_dataset()
    )

    payload = registry.to_dict()

    assert "cash_and_cash_equivalents" in payload
    assert "market_cap" in payload
    assert "reconciled_enterprise_value" in payload
