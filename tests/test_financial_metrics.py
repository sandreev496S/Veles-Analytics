from services.analysis.financial_metrics import (
    BalanceSheetState,
    EnterpriseValueRelation,
    LiquidityState,
    build_financial_metrics,
    parse_runway_years,
)


def test_net_cash_metrics() -> None:
    metrics = build_financial_metrics(
        cash=1_000,
        debt=250,
    )

    assert metrics.net_position == 750
    assert metrics.net_cash == 750
    assert metrics.net_debt is None
    assert (
        metrics.balance_sheet_state
        is BalanceSheetState.NET_CASH
    )


def test_net_debt_metrics() -> None:
    metrics = build_financial_metrics(
        cash=275,
        debt=1_000,
    )

    assert metrics.net_position == -725
    assert metrics.net_cash is None
    assert metrics.net_debt == 725
    assert (
        metrics.balance_sheet_state
        is BalanceSheetState.NET_DEBT
    )


def test_missing_debt_remains_unknown() -> None:
    metrics = build_financial_metrics(
        cash=1_000,
        debt=None,
    )

    assert metrics.net_position is None
    assert (
        metrics.balance_sheet_state
        is BalanceSheetState.UNKNOWN
    )


def test_enterprise_value_above_market_cap() -> None:
    metrics = build_financial_metrics(
        cash=100,
        debt=500,
        market_cap=2_000,
        enterprise_value=2_400,
    )

    assert (
        metrics.enterprise_value_relation
        is EnterpriseValueRelation.ABOVE_MARKET_CAP
    )


def test_runway_months_convert_to_years() -> None:
    assert parse_runway_years("18 months") == 1.5


def test_strong_liquidity_requires_net_cash() -> None:
    metrics = build_financial_metrics(
        cash=1_000,
        debt=100,
        free_cash_flow=-100,
        estimated_runway="2.5 years",
    )

    assert metrics.liquidity_state is LiquidityState.STRONG


def test_net_debt_with_runway_is_only_adequate() -> None:
    metrics = build_financial_metrics(
        cash=100,
        debt=1_000,
        free_cash_flow=-100,
        estimated_runway="2.5 years",
    )

    assert metrics.liquidity_state is LiquidityState.ADEQUATE
