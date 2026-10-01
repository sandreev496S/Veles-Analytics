from pathlib import Path

path = Path("app.py")
text = path.read_text()

replacements = {
    'st.subheader("rNPV Valuation Summary")':
    'section_title("rNPV Valuation Summary", "Probability-adjusted enterprise value, equity value, implied share price, and approval risk.")',

    'st.subheader("Probability-Adjusted Forecast")':
    'section_title("Probability-Adjusted Forecast", "Projected revenue, operating profit, free cash flow, and risk-adjusted value.")',

    'st.subheader("rNPV Sensitivity Matrix — Implied Share Price")':
    'section_title("Sensitivity Analysis", "Implied share price sensitivity across probability and discount-rate assumptions.")',

    'st.subheader("Monte Carlo rNPV Simulation")':
    'section_title("Risk Analysis", "Monte Carlo simulation, valuation distribution, percentile outcomes, and scenario risk.")',

    'st.subheader("Monte Carlo Percentiles")':
    'section_title("Monte Carlo Percentiles", "Distribution percentiles for simulated enterprise value outcomes.")',

    'st.subheader("Tornado Analysis — Key Valuation Drivers")':
    'section_title("Key Valuation Drivers", "Variables with the greatest impact on enterprise value.")',

    'st.subheader("Monte Carlo CDF — Probability Valuation Is Below Threshold")':
    'section_title("Monte Carlo CDF", "Probability that simulated enterprise value falls below or exceeds a selected threshold.")',
}

for old, new in replacements.items():
    text = text.replace(old, new, 1)

path.write_text(text)
print("rNPV section titles polished.")
