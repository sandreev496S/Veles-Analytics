from services.reports.equity_report_assembler import (
    assemble_equity_report,
)


def test_report_generates_core_financial_charts():
    report = assemble_equity_report("RXRX")

    expected = {
        "revenue_trend",
        "rd_expense_trend",
        "operating_net_loss_trend",
        "cash_vs_debt",
    }

    assert expected.issubset(
        report.charts.keys()
    )


def test_market_cap_vs_ev_chart_when_live_inputs_exist():
    report = assemble_equity_report("RXRX")

    market_snapshot = (
        report.market_snapshot or []
    )

    available_metrics = {
        str(row[0]).strip()
        for row in market_snapshot[1:]
        if row and len(row) > 1
    }

    required_inputs = {
        "Market Cap",
        "Enterprise Value",
    }

    if required_inputs.issubset(
        available_metrics
    ):
        assert (
            "market_cap_vs_ev"
            in report.charts
        )
