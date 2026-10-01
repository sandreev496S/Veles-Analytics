from services.valuation.valuation_report_adapter import (
    adapt_saved_valuation_for_report,
)


def test_adapter_handles_missing_valuation():
    result = adapt_saved_valuation_for_report(None)

    assert result["status"] == "unavailable"


def test_adapter_builds_report_tables():
    saved = {
        "name": "Base DCF",
        "saved_at": "2026-07-11T12:00:00Z",
        "payload": {
            "snapshot": {
                "share_price": {
                    "value": 10.0,
                }
            },
            "base_result": {
                "enterprise_value": 800_000_000,
                "equity_value": 1_000_000_000,
                "implied_value_per_share": 12.50,
                "wacc": 0.10,
                "present_value_forecast_fcf": 150_000_000,
                "present_value_terminal_value": 650_000_000,
                "forecast": [
                    {
                        "year": 2026,
                        "revenue": 120_000_000,
                        "revenue_growth": 0.20,
                        "ebit_margin": -0.30,
                        "ebit": -36_000_000,
                        "unlevered_fcf": -40_000_000,
                        "present_value_fcf": -36_000_000,
                    }
                ],
                "assumptions": {
                    "terminal_growth_rate": 0.025,
                },
            },
            "scenarios": {
                "bull": {
                    "enterprise_value": 1_000_000_000,
                    "equity_value": 1_200_000_000,
                    "implied_value_per_share": 15.0,
                },
                "base": {
                    "enterprise_value": 800_000_000,
                    "equity_value": 1_000_000_000,
                    "implied_value_per_share": 12.5,
                },
                "bear": {
                    "enterprise_value": 500_000_000,
                    "equity_value": 700_000_000,
                    "implied_value_per_share": 8.75,
                },
            },
            "sensitivity": {
                "wacc_values": [0.09],
                "terminal_growth_values": [0.02],
                "cells": [
                    {
                        "wacc": 0.09,
                        "terminal_growth_rate": 0.02,
                        "implied_value_per_share": 13.5,
                    }
                ],
            },
            "assumption_build": {
                "assumptions": {
                    "risk_free_rate": 0.04,
                    "equity_risk_premium": 0.055,
                    "beta": 1.2,
                    "cost_of_debt": 0.07,
                    "debt_weight": 0.10,
                    "equity_weight": 0.90,
                    "terminal_growth_rate": 0.025,
                    "cash": 250_000_000,
                    "debt": 50_000_000,
                    "diluted_shares_outstanding": 80_000_000,
                },
                "warnings": [],
            },
        },
    }

    result = adapt_saved_valuation_for_report(
        saved
    )

    assert result["status"] == "available"
    assert result["summary"][
        "implied_value_per_share"
    ] == "$12.50"
    assert len(result["scenario_table"]) == 4
    assert len(result["forecast_table"]) == 2
    assert result["sensitivity_table"]


def test_assumption_table_includes_terminal_ebit_margin():
    saved = {
        "name": "Illustrative Driver DCF",
        "payload": {
            "model_status": "illustrative",
            "forecast_years": 10,
            "snapshot": {
                "share_price": {
                    "value": 10.0,
                }
            },
            "base_result": {
                "enterprise_value": 800_000_000,
                "equity_value": 1_000_000_000,
                "implied_value_per_share": 12.50,
                "wacc": 0.10,
                "present_value_forecast_fcf": 150_000_000,
                "present_value_terminal_value": 650_000_000,
                "forecast": [
                    {
                        "year": 2035,
                        "total_revenue": 1_000_000_000,
                        "revenue_growth": 0.10,
                        "ebit_margin": 0.636,
                        "ebit": 636_000_000,
                        "unlevered_fcf": 500_000_000,
                        "present_value_fcf": 200_000_000,
                    }
                ],
                "assumptions": {
                    "terminal_growth_rate": 0.025,
                },
            },
            "scenarios": {
                "bull": {
                    "enterprise_value": 1_000_000_000,
                    "equity_value": 1_200_000_000,
                    "implied_value_per_share": 15.0,
                },
                "base": {
                    "enterprise_value": 800_000_000,
                    "equity_value": 1_000_000_000,
                    "implied_value_per_share": 12.5,
                },
                "bear": {
                    "enterprise_value": 500_000_000,
                    "equity_value": 700_000_000,
                    "implied_value_per_share": 8.75,
                },
            },
            "sensitivity": {
                "wacc_values": [0.09],
                "terminal_growth_values": [0.02],
                "cells": [
                    {
                        "wacc": 0.09,
                        "terminal_growth_rate": 0.02,
                        "implied_value_per_share": 13.5,
                    }
                ],
            },
            "assumption_build": {
                "assumptions": {
                    "risk_free_rate": 0.04,
                    "equity_risk_premium": 0.055,
                    "beta": 1.2,
                    "cost_of_debt": 0.07,
                    "debt_weight": 0.10,
                    "equity_weight": 0.90,
                    "terminal_growth_rate": 0.025,
                    "cash": 250_000_000,
                    "debt": 50_000_000,
                    "diluted_shares_outstanding": 80_000_000,
                },
                "warnings": [],
            },
        },
    }

    result = adapt_saved_valuation_for_report(saved)

    terminal_rows = [
        row
        for row in result["assumption_table"]
        if row[0] == "Terminal-Year EBIT Margin"
    ]

    assert terminal_rows == [
        [
            "Terminal-Year EBIT Margin",
            "63.6%",
            "Derived model output",
        ]
    ]
