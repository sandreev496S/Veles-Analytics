from services.valuation.valuation_report_adapter import (
    adapt_saved_valuation_for_report,
)


def complete_saved_valuation():
    assumptions = {
        "risk_free_rate": 0.04,
        "equity_risk_premium": 0.055,
        "beta": 1.0,
        "cost_of_debt": 0.07,
        "debt_weight": 0.05,
        "equity_weight": 0.95,
        "terminal_growth_rate": 0.025,
        "cash": 743_000_000,
        "debt": 78_000_000,
        "diluted_shares_outstanding": 530_000_000,
    }

    base_result = {
        "enterprise_value": 2_000_000_000,
        "equity_value": 2_665_000_000,
        "implied_value_per_share": 5.03,
        "wacc": 0.095,
        "present_value_forecast_fcf": -300_000_000,
        "present_value_terminal_value": 2_300_000_000,
        "forecast": [
            {
                "year": year,
                "revenue": 100_000_000 * index,
                "revenue_growth": 0.20,
                "ebit_margin": -1.0 + index * 0.20,
                "ebit": -50_000_000,
                "unlevered_fcf": -60_000_000,
                "present_value_fcf": -50_000_000,
            }
            for index, year in enumerate(
                range(2026, 2031),
                start=1,
            )
        ],
        "assumptions": assumptions,
    }

    scenarios = {
        name: {
            "enterprise_value": value,
            "equity_value": value + 665_000_000,
            "implied_value_per_share": (
                value + 665_000_000
            ) / 530_000_000,
        }
        for name, value in {
            "bull": 3_000_000_000,
            "base": 2_000_000_000,
            "bear": 1_000_000_000,
        }.items()
    }

    sensitivity = {
        "wacc_values": [0.09, 0.10],
        "terminal_growth_values": [0.02, 0.025],
        "cells": [
            {
                "wacc": wacc,
                "terminal_growth_rate": growth,
                "implied_value_per_share": 5.0,
            }
            for wacc in [0.09, 0.10]
            for growth in [0.02, 0.025]
        ],
    }

    return {
        "name": "RXRX Base DCF",
        "saved_at": "2026-07-11T12:00:00Z",
        "payload": {
            "snapshot": {
                "share_price": {
                    "value": 3.56,
                },
            },
            "base_result": base_result,
            "scenarios": scenarios,
            "sensitivity": sensitivity,
            "assumption_build": {
                "assumptions": assumptions,
                "warnings": [],
            },
        },
    }


def test_complete_dcf_report_layers():
    valuation = adapt_saved_valuation_for_report(
        complete_saved_valuation()
    )

    assert valuation["status"] == "available"
    assert len(valuation["scenario_table"]) == 4
    assert len(valuation["forecast_table"]) == 6
    assert len(valuation["sensitivity_table"]) == 3
    assert len(valuation["assumption_table"]) > 5
    assert (
        valuation["summary"][
            "implied_value_per_share"
        ]
        != "N/A"
    )


def test_incomplete_dcf_is_rejected():
    valuation = adapt_saved_valuation_for_report({
        "payload": {
            "base_result": {
                "enterprise_value": 1,
            }
        }
    })

    assert valuation["status"] == "invalid"
    assert valuation["missing_layers"]
