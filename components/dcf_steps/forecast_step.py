import streamlit as st
from components.ui.cards import glass_card


DEFAULT_DCF_SCENARIOS = {
    # Generic fallback only.
    # Company-specific historicals should overwrite these values.
    "Worst Case": {
        "growth": 0.05,
        "ebit_margin": 0.10,
        "tax_rate": 0.21,
        "da_pct": 0.03,
        "capex_pct": 0.05,
        "nwc_pct": 0.02,
    },
    "Base Case": {
        "growth": 0.10,
        "ebit_margin": 0.15,
        "tax_rate": 0.21,
        "da_pct": 0.03,
        "capex_pct": 0.04,
        "nwc_pct": 0.01,
    },
    "Best Case": {
        "growth": 0.15,
        "ebit_margin": 0.20,
        "tax_rate": 0.21,
        "da_pct": 0.03,
        "capex_pct": 0.03,
        "nwc_pct": 0.01,
    },
}


def render_forecast_step():
    glass_card(
        title="Forecast Assumptions Matrix",
        eyebrow="Forecast",
        body="Compare downside, base, and upside assumptions horizontally across growth, profitability, taxes, reinvestment, and working capital."
    )

    pending_historical_inputs = st.session_state.pop("pending_historical_forecast_inputs", None)

    if pending_historical_inputs:
        growth = pending_historical_inputs.get("growth")
        ebit_margin = pending_historical_inputs.get("ebit_margin")
        fcf_conversion = pending_historical_inputs.get("fcf_conversion")
        capex_pct = pending_historical_inputs.get("capex_pct")

        if growth is not None:
            raw_growth = float(growth)

            # Historical hypergrowth should not be blindly projected forward.
            # Use a tapered and capped forward growth seed.
            if raw_growth > 0.50:
                base_growth = 0.30
            elif raw_growth > 0.30:
                base_growth = raw_growth * 0.70
            else:
                base_growth = raw_growth

            base_growth = max(min(base_growth, 0.30), -0.10)

            st.session_state["dcf_Worst Case_growth"] = max(base_growth - 0.05, -0.10)
            st.session_state["dcf_Base Case_growth"] = base_growth
            st.session_state["dcf_Best Case_growth"] = min(base_growth + 0.05, 0.40)

        if ebit_margin is not None:
            st.session_state["dcf_Worst Case_ebit_margin"] = max(float(ebit_margin) - 0.05, 0.0)
            st.session_state["dcf_Base Case_ebit_margin"] = float(ebit_margin)
            st.session_state["dcf_Best Case_ebit_margin"] = min(float(ebit_margin) + 0.05, 1.0)

        # Capital intensity should come from historical CapEx,
        # not from a generic FCF-conversion percentage.
        if capex_pct is not None:
            base_capex = max(
                0.0,
                min(float(capex_pct), 0.20),
            )

            st.session_state[
                "dcf_Worst Case_capex_pct"
            ] = min(base_capex + 0.01, 0.25)

            st.session_state[
                "dcf_Base Case_capex_pct"
            ] = base_capex

            st.session_state[
                "dcf_Best Case_capex_pct"
            ] = max(base_capex - 0.01, 0.0)

        # D&A and NWC remain explicit user-adjustable assumptions.
        # Do not infer them from FCF conversion.
        if fcf_conversion is not None:
            st.session_state.setdefault(
                "dcf_Worst Case_da_pct", 0.03
            )
            st.session_state.setdefault(
                "dcf_Base Case_da_pct", 0.03
            )
            st.session_state.setdefault(
                "dcf_Best Case_da_pct", 0.03
            )

            st.session_state.setdefault(
                "dcf_Worst Case_nwc_pct", 0.02
            )
            st.session_state.setdefault(
                "dcf_Base Case_nwc_pct", 0.01
            )
            st.session_state.setdefault(
                "dcf_Best Case_nwc_pct", 0.01
            )

        st.success("Historical trends applied to forecast assumptions.")

    scenarios = {
        scenario_name: {}
        for scenario_name in DEFAULT_DCF_SCENARIOS.keys()
    }

    assumption_groups = [
        (
            "Revenue Growth",
            "Top-line growth by scenario.",
            ["growth"],
        ),
        (
            "Operating Profitability",
            "EBIT margin and tax assumptions.",
            ["ebit_margin", "tax_rate"],
        ),
        (
            "FCF Conversion",
            "Depreciation, capital expenditure, and working capital intensity.",
            ["da_pct", "capex_pct", "nwc_pct"],
        ),
    ]

    for group_title, group_caption, keys in assumption_groups:
        st.markdown(f"### {group_title}")
        st.caption(group_caption)

        header_cols = st.columns([1.25, 1, 1, 1])

        with header_cols[0]:
            st.markdown("**Assumption**")

        for idx, scenario_name in enumerate(DEFAULT_DCF_SCENARIOS.keys()):
            with header_cols[idx + 1]:
                st.markdown(f"**{scenario_name}**")

        for key in keys:
            row_cols = st.columns([1.25, 1, 1, 1])
            label = key.replace("_", " ").title()

            with row_cols[0]:
                st.markdown(f"**{label}**")

            for idx, scenario_name in enumerate(DEFAULT_DCF_SCENARIOS.keys()):
                default = DEFAULT_DCF_SCENARIOS[scenario_name][key]
                state_key = f"dcf_{scenario_name}_{key}"

                if state_key not in st.session_state:
                    st.session_state[state_key] = default

                with row_cols[idx + 1]:
                    scenarios[scenario_name][key] = st.number_input(
                        f"{scenario_name} {label}",
                        format="%.3f",
                        key=state_key,
                        label_visibility="collapsed",
                    )

        st.markdown("---")

    return scenarios

def get_scenarios_from_state():
    scenarios = {}

    for scenario_name, assumptions in DEFAULT_DCF_SCENARIOS.items():
        scenarios[scenario_name] = {}

        for key, default in assumptions.items():
            scenarios[scenario_name][key] = st.session_state.get(
                f"dcf_{scenario_name}_{key}",
                default,
            )

    return scenarios
