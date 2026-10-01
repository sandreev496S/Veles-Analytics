from pathlib import Path

from services.valuation.persistence import (
    list_saved_valuations,
    load_latest_valuation,
    load_valuation,
    save_valuation,
)


def complete_payload():
    assumptions = {
        "risk_free_rate": 0.04,
        "equity_risk_premium": 0.055,
        "beta": 1.0,
        "cost_of_debt": 0.07,
        "debt_weight": 0.05,
        "equity_weight": 0.95,
        "terminal_growth_rate": 0.025,
        "cash": 100.0,
        "debt": 20.0,
        "diluted_shares_outstanding": 50.0,
    }

    return {
        "snapshot": {
            "share_price": {
                "value": 3.5,
            }
        },
        "base_result": {
            "enterprise_value": 100.0,
            "equity_value": 180.0,
            "implied_value_per_share": 3.6,
            "wacc": 0.10,
            "present_value_forecast_fcf": 20.0,
            "present_value_terminal_value": 80.0,
            "forecast": [
                {
                    "year": 2026,
                    "revenue": 120.0,
                    "revenue_growth": 0.20,
                    "ebit_margin": 0.10,
                    "ebit": 12.0,
                    "unlevered_fcf": 10.0,
                    "present_value_fcf": 9.0,
                }
            ],
            "assumptions": assumptions,
        },
        "scenarios": {
            "bull": {
                "enterprise_value": 130.0,
                "equity_value": 210.0,
                "implied_value_per_share": 4.2,
            },
            "base": {
                "enterprise_value": 100.0,
                "equity_value": 180.0,
                "implied_value_per_share": 3.6,
            },
            "bear": {
                "enterprise_value": 70.0,
                "equity_value": 150.0,
                "implied_value_per_share": 3.0,
            },
        },
        "sensitivity": {
            "wacc_values": [0.09],
            "terminal_growth_values": [0.02],
            "cells": [
                {
                    "wacc": 0.09,
                    "terminal_growth_rate": 0.02,
                    "enterprise_value": 110.0,
                    "equity_value": 190.0,
                    "implied_value_per_share": 3.8,
                }
            ],
        },
        "assumption_build": {
            "assumptions": assumptions,
            "warnings": [],
        },
    }


def test_save_and_load_valuation(
    tmp_path,
    monkeypatch,
):
    import services.valuation.persistence as persistence

    monkeypatch.setattr(
        persistence,
        "VALUATION_ROOT",
        tmp_path,
    )

    path = save_valuation(
        ticker="TEST",
        payload=complete_payload(),
        name="Test DCF",
    )

    assert Path(path).exists()

    loaded = load_valuation(path)

    assert loaded["ticker"] == "TEST"
    assert loaded["name"] == "Test DCF"
    assert (
        loaded["payload"]["base_result"][
            "implied_value_per_share"
        ]
        == 3.6
    )

    saved = list_saved_valuations("TEST")

    assert len(saved) == 1
    assert load_latest_valuation("TEST") is not None


def test_incomplete_valuation_cannot_be_saved(
    tmp_path,
    monkeypatch,
):
    import pytest
    import services.valuation.persistence as persistence

    from services.valuation.integration_validation import (
        DCFIntegrationError,
    )

    monkeypatch.setattr(
        persistence,
        "VALUATION_ROOT",
        tmp_path,
    )

    with pytest.raises(DCFIntegrationError):
        save_valuation(
            ticker="TEST",
            payload={
                "base_result": {
                    "implied_value_per_share": 12.5,
                }
            },
            name="Incomplete DCF",
        )
