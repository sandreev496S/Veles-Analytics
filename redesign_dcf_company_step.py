from pathlib import Path

path = Path("components/dcf_steps/company_step.py")
text = path.read_text()

old = '''def render_company_step(section_title):
    section_title(
        "Step 1 — Company Information",
        "Enter the company profile and starting financial position."
    )

    glass_card(
        title="Company Starting Point",
        eyebrow="Company",
        body="Enter the core financial position that anchors the valuation: market capitalization, net cash or debt, diluted shares, current revenue, and forecast horizon."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        company_name = st.text_input(
            "Company name",
            value=st.session_state.get("dcf_company_name", "Adobe"),
            key="dcf_company_name",
        )

        current_market_cap = st.number_input(
            "Current market cap ($M)",
            value=st.session_state.get("dcf_current_market_cap", 170000.0),
            key="dcf_current_market_cap",
        )

        cash = st.number_input(
            "Cash & equivalents ($M)",
            value=st.session_state.get("dcf_cash", 7000.0),
            key="dcf_cash",
        )

    with col2:
        debt = st.number_input(
            "Total debt ($M)",
            value=st.session_state.get("dcf_debt", 6000.0),
            key="dcf_debt",
        )

        shares = st.number_input(
            "Diluted shares outstanding (M)",
            value=st.session_state.get("dcf_shares", 420.0),
            key="dcf_shares",
        )

        starting_revenue = st.number_input(
            "Starting revenue ($M)",
            value=st.session_state.get("dcf_starting_revenue", 23000.0),
            key="dcf_starting_revenue",
        )

    with col3:
        forecast_years = st.slider(
            "Forecast years",
            3,
            10,
            st.session_state.get("dcf_forecast_years", 5),
            key="dcf_forecast_years",
        )

    return {
        "company_name": company_name,
        "current_market_cap": current_market_cap,
        "cash": cash,
        "debt": debt,
        "shares": shares,
        "starting_revenue": starting_revenue,
        "forecast_years": forecast_years,
    }
'''

new = '''def render_company_step(section_title):
    section_title(
        "Step 1 — Company Setup",
        "Define the company profile, capital structure, and initial forecast base."
    )

    glass_card(
        title="Valuation Starting Point",
        eyebrow="Company Profile",
        body="Set the core assumptions that anchor the DCF: company name, current market value, cash, debt, diluted share count, revenue base, and forecast horizon."
    )

    profile_col, capital_col = st.columns([1, 1])

    with profile_col:
        section_title(
            "Company Profile",
            "Identity and forecast horizon."
        )

        company_name = st.text_input(
            "Company name",
            value=st.session_state.get("dcf_company_name", "Adobe"),
            key="dcf_company_name",
        )

        forecast_years = st.slider(
            "Forecast years",
            3,
            10,
            st.session_state.get("dcf_forecast_years", 5),
            key="dcf_forecast_years",
        )

        starting_revenue = st.number_input(
            "Starting revenue ($M)",
            value=st.session_state.get("dcf_starting_revenue", 23000.0),
            key="dcf_starting_revenue",
        )

    with capital_col:
        section_title(
            "Capital Structure",
            "Market value, liquidity, leverage, and share count."
        )

        current_market_cap = st.number_input(
            "Current market cap ($M)",
            value=st.session_state.get("dcf_current_market_cap", 170000.0),
            key="dcf_current_market_cap",
        )

        cash = st.number_input(
            "Cash & equivalents ($M)",
            value=st.session_state.get("dcf_cash", 7000.0),
            key="dcf_cash",
        )

        debt = st.number_input(
            "Total debt ($M)",
            value=st.session_state.get("dcf_debt", 6000.0),
            key="dcf_debt",
        )

        shares = st.number_input(
            "Diluted shares outstanding (M)",
            value=st.session_state.get("dcf_shares", 420.0),
            key="dcf_shares",
        )

    return {
        "company_name": company_name,
        "current_market_cap": current_market_cap,
        "cash": cash,
        "debt": debt,
        "shares": shares,
        "starting_revenue": starting_revenue,
        "forecast_years": forecast_years,
    }
'''

if old not in text:
    raise SystemExit("Could not find current render_company_step block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("DCF company step redesigned.")
