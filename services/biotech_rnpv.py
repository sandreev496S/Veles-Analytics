import pandas as pd


def run_biotech_rnpv(
    asset_name,
    launch_year,
    forecast_years,
    eligible_patients,
    price_per_treatment,
    peak_penetration,
    years_to_peak,
    probability_of_approval,
    operating_margin,
    tax_rate,
    discount_rate,
    annual_rd_cost,
    launch_cost,
    cash,
    debt,
    shares,
):
    rows = []
    pv_total = 0

    for year in range(1, forecast_years + 1):
        if year < launch_year:
            penetration = 0
            revenue = 0
            operating_profit = -annual_rd_cost

        else:
            years_since_launch = year - launch_year + 1
            penetration = min(
                peak_penetration,
                peak_penetration * years_since_launch / years_to_peak
            )
            treated_patients = eligible_patients * penetration
            revenue = treated_patients * price_per_treatment / 1_000_000
            operating_profit = revenue * operating_margin

            if year == launch_year:
                operating_profit -= launch_cost

        tax = max(operating_profit, 0) * tax_rate
        after_tax_profit = operating_profit - tax
        probability_adjusted_cash_flow = after_tax_profit * probability_of_approval

        pv = probability_adjusted_cash_flow / ((1 + discount_rate) ** year)
        pv_total += pv

        rows.append({
            "Year": year,
            "Penetration": penetration,
            "Revenue ($M)": revenue,
            "Operating Profit ($M)": operating_profit,
            "After-Tax Profit ($M)": after_tax_profit,
            "Probability-Adjusted CF ($M)": probability_adjusted_cash_flow,
            "PV rNPV CF ($M)": pv,
        })

    enterprise_value = pv_total
    equity_value = enterprise_value + cash - debt
    implied_share_price = equity_value / shares

    valuation = {
        "Asset rNPV / Enterprise Value ($M)": enterprise_value,
        "Equity Value ($M)": equity_value,
        "Implied Share Price ($)": implied_share_price,
        "Probability of Approval": probability_of_approval,
    }

    return pd.DataFrame(rows), valuation


def rnpv_sensitivity_matrix(
    asset_name,
    launch_year,
    forecast_years,
    eligible_patients,
    price_per_treatment,
    peak_penetration,
    years_to_peak,
    operating_margin,
    tax_rate,
    annual_rd_cost,
    launch_cost,
    cash,
    debt,
    shares,
):
    probabilities = [0.10, 0.20, 0.30, 0.40, 0.50]
    discount_rates = [0.12, 0.15, 0.18, 0.21, 0.25]

    matrix = {}

    for discount_rate in discount_rates:
        row = {}

        for probability in probabilities:
            _, valuation = run_biotech_rnpv(
                asset_name=asset_name,
                launch_year=launch_year,
                forecast_years=forecast_years,
                eligible_patients=eligible_patients,
                price_per_treatment=price_per_treatment,
                peak_penetration=peak_penetration,
                years_to_peak=years_to_peak,
                probability_of_approval=probability,
                operating_margin=operating_margin,
                tax_rate=tax_rate,
                discount_rate=discount_rate,
                annual_rd_cost=annual_rd_cost,
                launch_cost=launch_cost,
                cash=cash,
                debt=debt,
                shares=shares,
            )

            row[f"{probability:.0%}"] = valuation["Implied Share Price ($)"]

        matrix[f"{discount_rate:.0%}"] = row

    return pd.DataFrame(matrix).T


def run_monte_carlo_rnpv(
    asset_name,
    launch_year,
    forecast_years,
    eligible_patients,
    base_price_per_treatment,
    base_peak_penetration,
    years_to_peak,
    base_probability_of_approval,
    base_operating_margin,
    tax_rate,
    base_discount_rate,
    annual_rd_cost,
    launch_cost,
    cash,
    debt,
    shares,
    current_market_cap,
    simulations=10000,
    seed=42,
):
    import numpy as np

    rng = np.random.default_rng(seed)
    results = []

    for _ in range(simulations):
        probability = rng.triangular(
            max(0.01, base_probability_of_approval * 0.50),
            base_probability_of_approval,
            min(0.95, base_probability_of_approval * 1.75),
        )

        penetration = rng.triangular(
            max(0.001, base_peak_penetration * 0.40),
            base_peak_penetration,
            min(0.80, base_peak_penetration * 2.00),
        )

        price = rng.triangular(
            base_price_per_treatment * 0.70,
            base_price_per_treatment,
            base_price_per_treatment * 1.30,
        )

        margin = rng.triangular(
            max(0.01, base_operating_margin * 0.60),
            base_operating_margin,
            min(0.85, base_operating_margin * 1.35),
        )

        discount_rate = np.clip(
            rng.normal(base_discount_rate, 0.03),
            0.08,
            0.35,
        )

        _, valuation = run_biotech_rnpv(
            asset_name=asset_name,
            launch_year=launch_year,
            forecast_years=forecast_years,
            eligible_patients=eligible_patients,
            price_per_treatment=price,
            peak_penetration=penetration,
            years_to_peak=years_to_peak,
            probability_of_approval=probability,
            operating_margin=margin,
            tax_rate=tax_rate,
            discount_rate=discount_rate,
            annual_rd_cost=annual_rd_cost,
            launch_cost=launch_cost,
            cash=cash,
            debt=debt,
            shares=shares,
        )

        results.append({
            "Enterprise Value ($M)": valuation["Asset rNPV / Enterprise Value ($M)"],
            "Equity Value ($M)": valuation["Equity Value ($M)"],
            "Share Price ($)": valuation["Implied Share Price ($)"],
            "Probability of Approval": probability,
            "Peak Penetration": penetration,
            "Price per Treatment": price,
            "Operating Margin": margin,
            "Discount Rate": discount_rate,
        })

    results_df = pd.DataFrame(results)

    summary = {
        "Expected Enterprise Value ($M)": results_df["Enterprise Value ($M)"].mean(),
        "Expected Equity Value ($M)": results_df["Equity Value ($M)"].mean(),
        "Expected Share Price ($)": results_df["Share Price ($)"].mean(),
        "5th Percentile EV ($M)": results_df["Enterprise Value ($M)"].quantile(0.05),
        "25th Percentile EV ($M)": results_df["Enterprise Value ($M)"].quantile(0.25),
        "Median EV ($M)": results_df["Enterprise Value ($M)"].quantile(0.50),
        "75th Percentile EV ($M)": results_df["Enterprise Value ($M)"].quantile(0.75),
        "95th Percentile EV ($M)": results_df["Enterprise Value ($M)"].quantile(0.95),
        "Probability EV > Current Market Cap": (results_df["Enterprise Value ($M)"] > current_market_cap).mean(),
        "Probability EV < Cash": (results_df["Enterprise Value ($M)"] < cash).mean(),
    }

    return results_df, summary


def biotech_tornado_analysis(
    asset_name,
    launch_year,
    forecast_years,
    eligible_patients,
    price_per_treatment,
    peak_penetration,
    years_to_peak,
    probability_of_approval,
    operating_margin,
    tax_rate,
    discount_rate,
    annual_rd_cost,
    launch_cost,
    cash,
    debt,
    shares,
    shock=0.20,
):
    base_df, base_valuation = run_biotech_rnpv(
        asset_name=asset_name,
        launch_year=launch_year,
        forecast_years=forecast_years,
        eligible_patients=eligible_patients,
        price_per_treatment=price_per_treatment,
        peak_penetration=peak_penetration,
        years_to_peak=years_to_peak,
        probability_of_approval=probability_of_approval,
        operating_margin=operating_margin,
        tax_rate=tax_rate,
        discount_rate=discount_rate,
        annual_rd_cost=annual_rd_cost,
        launch_cost=launch_cost,
        cash=cash,
        debt=debt,
        shares=shares,
    )

    base_ev = base_valuation["Asset rNPV / Enterprise Value ($M)"]

    variables = {
        "Price per Treatment": "price_per_treatment",
        "Peak Penetration": "peak_penetration",
        "Probability of Approval": "probability_of_approval",
        "Operating Margin": "operating_margin",
        "Discount Rate": "discount_rate",
    }

    base_inputs = {
        "price_per_treatment": price_per_treatment,
        "peak_penetration": peak_penetration,
        "probability_of_approval": probability_of_approval,
        "operating_margin": operating_margin,
        "discount_rate": discount_rate,
    }

    rows = []

    for label, key in variables.items():
        low_inputs = base_inputs.copy()
        high_inputs = base_inputs.copy()

        low_inputs[key] = base_inputs[key] * (1 - shock)
        high_inputs[key] = base_inputs[key] * (1 + shock)

        if key in ["peak_penetration", "probability_of_approval", "operating_margin"]:
            low_inputs[key] = max(0.001, low_inputs[key])
            high_inputs[key] = min(0.95, high_inputs[key])

        if key == "discount_rate":
            low_inputs[key] = max(0.01, low_inputs[key])

        _, low_val = run_biotech_rnpv(
            asset_name=asset_name,
            launch_year=launch_year,
            forecast_years=forecast_years,
            eligible_patients=eligible_patients,
            price_per_treatment=low_inputs["price_per_treatment"],
            peak_penetration=low_inputs["peak_penetration"],
            years_to_peak=years_to_peak,
            probability_of_approval=low_inputs["probability_of_approval"],
            operating_margin=low_inputs["operating_margin"],
            tax_rate=tax_rate,
            discount_rate=low_inputs["discount_rate"],
            annual_rd_cost=annual_rd_cost,
            launch_cost=launch_cost,
            cash=cash,
            debt=debt,
            shares=shares,
        )

        _, high_val = run_biotech_rnpv(
            asset_name=asset_name,
            launch_year=launch_year,
            forecast_years=forecast_years,
            eligible_patients=eligible_patients,
            price_per_treatment=high_inputs["price_per_treatment"],
            peak_penetration=high_inputs["peak_penetration"],
            years_to_peak=years_to_peak,
            probability_of_approval=high_inputs["probability_of_approval"],
            operating_margin=high_inputs["operating_margin"],
            tax_rate=tax_rate,
            discount_rate=high_inputs["discount_rate"],
            annual_rd_cost=annual_rd_cost,
            launch_cost=launch_cost,
            cash=cash,
            debt=debt,
            shares=shares,
        )

        low_ev = low_val["Asset rNPV / Enterprise Value ($M)"]
        high_ev = high_val["Asset rNPV / Enterprise Value ($M)"]

        rows.append({
            "Variable": label,
            "Low Case EV ($M)": low_ev,
            "Base EV ($M)": base_ev,
            "High Case EV ($M)": high_ev,
            "Impact Range ($M)": abs(high_ev - low_ev),
        })

    tornado_df = pd.DataFrame(rows).sort_values(
        "Impact Range ($M)",
        ascending=False,
    )

    return tornado_df
