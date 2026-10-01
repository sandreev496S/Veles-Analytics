import math
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


def get_company_snapshot(ticker):
    ticker = ticker.strip().upper()

    if not ticker:
        raise ValueError("Ticker is required.")

    stock = yf.Ticker(ticker)
    info = stock.get_info()

    if not info:
        raise ValueError(f"No company data found for ticker: {ticker}")

    company_name = info.get("longName") or info.get("shortName") or ticker
    market_cap = _to_millions(info.get("marketCap"))
    shares = _to_millions(info.get("sharesOutstanding"))
    revenue = _to_millions(info.get("totalRevenue"))
    cash = _to_millions(info.get("totalCash"))
    debt = _to_millions(info.get("totalDebt"))
    enterprise_value = _to_millions(info.get("enterpriseValue"))
    ebitda = _to_millions(info.get("ebitda"))
    net_income = _to_millions(info.get("netIncomeToCommon"))

    return {
        "ticker": ticker,
        "company_name": company_name,
        "market_cap": market_cap,
        "share_price": info.get("currentPrice") or info.get("regularMarketPrice"),
        "shares": shares,
        "revenue": revenue,
        "cash": cash,
        "debt": debt,
        "enterprise_value": enterprise_value,
        "ebitda": ebitda,
        "net_income": net_income,
        "revenue_growth": info.get("revenueGrowth"),
        "ebitda_margin": info.get("ebitdaMargins"),
        "beta": info.get("beta"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
    }
