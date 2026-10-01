from services.pdf_report_exporter import _figure_links


def test_figure_links_omit_missing_destinations():
    result = _figure_links(
        ["revenue_trend", "rd_expense_trend", "operating_net_loss_trend"],
        {"revenue_trend": 1, "operating_net_loss_trend": 2},
    )

    assert 'href="#figure_1"' in result
    assert 'href="#figure_2"' in result
    assert "Figure 3" not in result


def test_figure_links_follow_actual_renumbering():
    result = _figure_links(
        ["cash_vs_debt", "market_cap_vs_ev"],
        {"cash_vs_debt": 2, "market_cap_vs_ev": 3},
    )

    assert "Figure 2" in result
    assert "Figure 3" in result
    assert "Figure 4" not in result
    assert "Figure 5" not in result


def test_figure_links_return_empty_when_no_figures_exist():
    assert _figure_links(["revenue_trend"], {}) == ""
