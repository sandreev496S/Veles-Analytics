from pathlib import Path

from services.charts.financial_chart_engine import (
    generate_financial_charts,
)


def test_market_cap_vs_ev_chart_with_complete_fixture(
    tmp_path,
    monkeypatch,
):
    import services.charts.financial_chart_engine as charts

    if hasattr(charts, "CHART_ROOT"):
        monkeypatch.setattr(
            charts,
            "CHART_ROOT",
            tmp_path,
        )

    result = generate_financial_charts(
        ticker="TEST",
        income_statement=[],
        balance_sheet=[],
        market_snapshot=[
            ["Metric", "Value"],
            ["Market Cap", "$1.90B"],
            ["Enterprise Value", "$1.30B"],
        ],
        report_brand={},
    )

    assert "market_cap_vs_ev" in result

    output_path = Path(
        result["market_cap_vs_ev"]
    )

    assert output_path.exists()
    assert output_path.stat().st_size > 0
