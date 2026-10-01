from pathlib import Path

path = Path("components/dcf_steps/forecast_step.py")
text = path.read_text()

start = text.index("def render_forecast_step():")
end = text.index("\ndef get_scenarios_from_state():", start)

new_func = '''def render_forecast_step():
    glass_card(
        title="Forecast Assumptions Matrix",
        eyebrow="Forecast",
        body="Compare downside, base, and upside assumptions horizontally across growth, profitability, taxes, reinvestment, and working capital."
    )

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

                with row_cols[idx + 1]:
                    scenarios[scenario_name][key] = st.number_input(
                        f"{scenario_name} {label}",
                        value=st.session_state.get(state_key, default),
                        format="%.3f",
                        key=state_key,
                        label_visibility="collapsed",
                    )

        st.markdown("---")

    return scenarios
'''

text = text[:start] + new_func + text[end:]
path.write_text(text)

print("DCF forecast step redesigned as matrix.")
