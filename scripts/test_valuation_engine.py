import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from services.valuation import (
    DCFAssumptions,
    calculate_dcf,
    calculate_sensitivity,
    calculate_standard_scenarios,
)


def money(value: float) -> str:
    return f"${value / 1_000_000:,.1f}M"


def main() -> None:
    assumptions = DCFAssumptions(
        ticker="DEMO",
        base_year=2025,
        base_revenue=100_000_000,
        revenue_growth_rates=[
            0.20,
            0.18,
            0.15,
            0.12,
            0.10,
        ],
        ebit_margins=[
            -0.30,
            -0.15,
            0.00,
            0.10,
            0.18,
        ],
        tax_rate=0.21,
        depreciation_amortization_pct_revenue=0.04,
        capex_pct_revenue=0.05,
        nwc_pct_revenue_change=0.08,
        risk_free_rate=0.04,
        equity_risk_premium=0.055,
        beta=1.20,
        cost_of_debt=0.07,
        debt_weight=0.10,
        equity_weight=0.90,
        terminal_growth_rate=0.025,
        cash=250_000_000,
        debt=50_000_000,
        diluted_shares_outstanding=100_000_000,
    )

    result = calculate_dcf(assumptions)

    print("Ticker:", result.ticker)
    print("WACC:", f"{result.wacc:.2%}")
    print("Enterprise value:", money(result.enterprise_value))
    print("Equity value:", money(result.equity_value))
    print(
        "Implied value/share:",
        f"${result.implied_value_per_share:,.2f}",
    )

    print("\nForecast:")
    for year in result.forecast:
        print(
            year.year,
            money(year.revenue),
            f"EBIT margin {year.ebit_margin:.1%}",
            f"UFCF {money(year.unlevered_fcf)}",
        )

    print("\nScenarios:")
    for name, scenario in calculate_standard_scenarios(
        assumptions
    ).items():
        print(
            name,
            f"${scenario.implied_value_per_share:,.2f}",
        )

    sensitivity = calculate_sensitivity(
        assumptions,
        wacc_values=[0.09, 0.10, 0.11],
        terminal_growth_values=[0.02, 0.025, 0.03],
    )

    print("\nSensitivity cells:", len(sensitivity.cells))


if __name__ == "__main__":
    main()
