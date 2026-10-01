from pathlib import Path

path = Path("components/dcf_steps/scenarios_step.py")
text = path.read_text()

start = text.index("def render_scenarios_step():")
end = text.index("\ndef get_scenario_assumptions_from_state():", start)

new_func = '''def render_scenarios_step():
    glass_card(
        title="Valuation Parameters Matrix",
        eyebrow="Scenarios",
        body="Compare discount rate, terminal growth, and margin of safety assumptions horizontally across downside, base, and upside cases."
    )

    scenarios = {
        scenario_name: {}
        for scenario_name in DEFAULT_SCENARIO_ASSUMPTIONS.keys()
    }

    assumption_groups = [
        (
            "Discount Rate",
            "Required return used to discount projected free cash flow.",
            ["discount_rate"],
        ),
        (
            "Terminal Growth",
            "Long-term growth rate used to estimate terminal value.",
            ["terminal_growth"],
        ),
        (
            "Margin of Safety",
            "Discount applied to intrinsic value to define a more conservative buy threshold.",
            ["margin_of_safety"],
        ),
    ]

    for group_title, group_caption, keys in assumption_groups:
        st.markdown(f"### {group_title}")
        st.caption(group_caption)

        header_cols = st.columns([1.25, 1, 1, 1])

        with header_cols[0]:
            st.markdown("**Assumption**")

        for idx, scenario_name in enumerate(DEFAULT_SCENARIO_ASSUMPTIONS.keys()):
            with header_cols[idx + 1]:
                st.markdown(f"**{scenario_name}**")

        for key in keys:
            row_cols = st.columns([1.25, 1, 1, 1])
            label = key.replace("_", " ").title()

            with row_cols[0]:
                st.markdown(f"**{label}**")

            for idx, scenario_name in enumerate(DEFAULT_SCENARIO_ASSUMPTIONS.keys()):
                default = DEFAULT_SCENARIO_ASSUMPTIONS[scenario_name][key]
                state_key = f"dcf_scenario_{scenario_name}_{key}"

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

print("DCF scenarios step redesigned as matrix.")
