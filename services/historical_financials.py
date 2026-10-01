import math
import pandas as pd
import yfinance as yf


def _to_millions(value):
    if value is None:
        return None
    try:
        value = float(value)
    except Exception:
        return None
    if math.isnan(value):
        return None
    return value / 1_000_000


def _safe_series_statement_value(statement, possible_rows, column):
    for row in possible_rows:
        if row in statement.index:
            value = statement.loc[row, column]
            return _to_millions(value)
    return None


def _cagr(start_value, end_value, years):
    if not start_value or not end_value or start_value <= 0 or end_value <= 0 or years <= 0:
        return None
    return (end_value / start_value) ** (1 / years) - 1


def get_historical_financials(ticker):
    ticker = ticker.strip().upper()
    stock = yf.Ticker(ticker)

    income = stock.financials
    cashflow = stock.cashflow

    if income is None or income.empty:
        raise ValueError(f"No historical income statement data found for {ticker}.")

    years = list(income.columns)
    rows = []

    for col in years:
        year_label = str(col.year) if hasattr(col, "year") else str(col)

        revenue = _safe_series_statement_value(
            income,
            ["Total Revenue", "Operating Revenue"],
            col,
        )

        ebit = _safe_series_statement_value(
            income,
            ["EBIT", "Operating Income"],
            col,
        )

        net_income = _safe_series_statement_value(
            income,
            ["Net Income", "Net Income Common Stockholders"],
            col,
        )

        operating_cash_flow = None
        capex = None
        free_cash_flow = None

        if cashflow is not None and not cashflow.empty and col in cashflow.columns:
            operating_cash_flow = _safe_series_statement_value(
                cashflow,
                ["Operating Cash Flow", "Total Cash From Operating Activities"],
                col,
            )

            capex = _safe_series_statement_value(
                cashflow,
                ["Capital Expenditure", "Capital Expenditures"],
                col,
            )

            if operating_cash_flow is not None and capex is not None:
                free_cash_flow = operating_cash_flow + capex

        rows.append(
            {
                "Year": year_label,
                "Revenue ($M)": revenue,
                "EBIT ($M)": ebit,
                "Net Income ($M)": net_income,
                "Operating Cash Flow ($M)": operating_cash_flow,
                "CapEx ($M)": capex,
                "FCF ($M)": free_cash_flow,
            }
        )

    df = pd.DataFrame(rows).dropna(subset=["Revenue ($M)"])
    df = df.sort_values("Year")

    if df.empty:
        raise ValueError(f"No usable historical financials found for {ticker}.")

    first_revenue = df["Revenue ($M)"].iloc[0]
    last_revenue = df["Revenue ($M)"].iloc[-1]
    periods = len(df) - 1

    revenue_cagr = _cagr(first_revenue, last_revenue, periods)

    latest_revenue = df["Revenue ($M)"].iloc[-1]

    avg_ebit_margin = None
    if "EBIT ($M)" in df.columns:
        margin_series = df["EBIT ($M)"] / df["Revenue ($M)"]
        margin_series = margin_series.replace([float("inf"), -float("inf")], pd.NA).dropna()
        if not margin_series.empty:
            avg_ebit_margin = float(margin_series.mean())

    avg_fcf_conversion = None
    if "FCF ($M)" in df.columns:
        fcf_series = df["FCF ($M)"] / df["Revenue ($M)"]
        fcf_series = fcf_series.replace(
            [float("inf"), -float("inf")],
            pd.NA,
        ).dropna()
        if not fcf_series.empty:
            avg_fcf_conversion = float(fcf_series.mean())

    # Historical capital intensity.
    # Yahoo commonly reports CapEx as a negative cash-flow number,
    # so use absolute value when expressing CapEx as % of revenue.
    avg_capex_pct = None
    if "CapEx ($M)" in df.columns:
        capex_series = (
            df["CapEx ($M)"].abs()
            / df["Revenue ($M)"]
        )
        capex_series = capex_series.replace(
            [float("inf"), -float("inf")],
            pd.NA,
        ).dropna()

        if not capex_series.empty:
            avg_capex_pct = float(capex_series.mean())

    return {
        "ticker": ticker,
        "historical_df": df,
        "latest_revenue": latest_revenue,
        "revenue_cagr": revenue_cagr,
        "avg_ebit_margin": avg_ebit_margin,
        "avg_fcf_conversion": avg_fcf_conversion,
        "avg_capex_pct": avg_capex_pct,
    }
