from services.valuation.workspace import (
    ValuationWorkspaceState,
    build_default_workspace,
    run_workspace_valuation,
)


def research_fixture():
    return {
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
        "metadata": {},
    }


def test_default_workspace_builds():
    workspace = build_default_workspace(
        research_fixture()
    )

    assert isinstance(
        workspace,
        ValuationWorkspaceState,
    )
    assert workspace.ticker == "TEST"
    assert len(
        workspace.forecast_profile[
            "revenue_growth_rates"
        ]
    ) == 5


def test_workspace_runs_dcf():
    workspace = build_default_workspace(
        research_fixture()
    )

    result = run_workspace_valuation(
        research_fixture(),
        workspace,
    )

    assert not result.errors
    assert result.result is not None
    assert "base_result" in result.result
