from services.data_quality.validated_attachment import (
    attach_validated_metrics,
)


def test_attach_validated_metrics_adds_serialized_registry():
    research = {
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
                            "accession_number": (
                                "0001601830-26-000078"
                            ),
                            "value": 654_473_000,
                        }
                    ]
                }
            }
        },
    }

    result = attach_validated_metrics(research)

    assert result is research
    assert "validated_metrics" in result
    assert "validation_summary" in result

    cash = result["validated_metrics"][
        "cash_and_cash_equivalents"
    ]

    assert cash["value"] == 654_473_000
    assert cash["validation_status"] == "verified"

    summary = result["validation_summary"]

    assert summary["metric_count"] > 0
    assert (
        "reconciled_enterprise_value"
        in summary["withheld_metrics"]
    )
