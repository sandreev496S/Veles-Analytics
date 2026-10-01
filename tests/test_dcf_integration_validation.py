import pytest

from services.valuation.integration_validation import (
    DCFIntegrationError,
    validate_complete_dcf_payload,
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
        "cash": 100,
        "debt": 20,
        "diluted_shares_outstanding": 50,
    }

    return {
        "snapshot": {
            "share_price": {
                "value": 3.5,
            }
        },
        "base_result": {
            "enterprise_value": 100,
            "equity_value": 180,
            "implied_value_per_share": 3.6,
            "wacc": 0.10,
            "forecast": [
                {
                    "year": 2026,
                }
            ],
            "assumptions": assumptions,
        },
        "scenarios": {
            "bull": {
                "implied_value_per_share": 5.0,
            },
            "base": {
                "implied_value_per_share": 3.6,
            },
            "bear": {
                "implied_value_per_share": 2.0,
            },
        },
        "sensitivity": {
            "wacc_values": [0.09],
            "terminal_growth_values": [0.02],
            "cells": [
                {
                    "wacc": 0.09,
                    "terminal_growth_rate": 0.02,
                    "implied_value_per_share": 4.0,
                }
            ],
        },
        "assumption_build": {
            "assumptions": assumptions,
            "warnings": [],
        },
    }


def test_complete_payload_passes():
    assert validate_complete_dcf_payload(
        complete_payload()
    ) == []


def test_validator_accepts_nested_dictionaries():
    payload = complete_payload()

    assert isinstance(payload["base_result"], dict)
    assert isinstance(payload["assumption_build"], dict)
    assert validate_complete_dcf_payload(payload) == []


def test_missing_forecast_fails():
    payload = complete_payload()
    payload["base_result"]["forecast"] = []

    with pytest.raises(DCFIntegrationError):
        validate_complete_dcf_payload(payload)


def test_missing_scenario_fails():
    payload = complete_payload()
    del payload["scenarios"]["bear"]

    with pytest.raises(DCFIntegrationError):
        validate_complete_dcf_payload(payload)
