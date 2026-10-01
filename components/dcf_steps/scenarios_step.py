import streamlit as st
from components.ui.cards import glass_card
from components.dcf_steps.wacc_calculator import render_wacc_calculator


DEFAULT_SCENARIO_ASSUMPTIONS = {
    "Worst Case": {
        "discount_rate": 0.09,
        "terminal_growth": 0.02,
        "margin_of_safety": 0.35,
    },
    "Base Case": {
        "discount_rate": 0.09,
        "terminal_growth": 0.025,
        "margin_of_safety": 0.25,
    },
    "Best Case": {
        "discount_rate": 0.08,
        "terminal_growth": 0.03,
        "margin_of_safety": 0.20,
    },
}


def render_scenarios_step(default_equity_value=1000.0, default_debt_value=0.0):
    glass_card(
        title="Valuation Parameters Matrix",
        eyebrow="Scenarios",
        body="Compare discount rate, terminal growth, and margin of safety assumptions horizontally across downside, base, and upside cases."
    )

    render_wacc_calculator(
        default_equity_value=default_equity_value,
        default_debt_value=default_debt_value,
    )

    if "pending_base_case_wacc" in st.session_state:
        base_wacc = float(st.session_state.pop("pending_base_case_wacc"))

        st.session_state["dcf_scenario_Worst Case_discount_rate"] = min(base_wacc + 0.01, 0.30)
        st.session_state["dcf_scenario_Base Case_discount_rate"] = base_wacc
        st.session_state["dcf_scenario_Best Case_discount_rate"] = max(base_wacc - 0.01, 0.01)

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

    # Persist the exact values rendered in Step 3.
    #
    # The number_input keys are widget-owned and may disappear when
    # navigating to Step 4. This non-widget snapshot survives and is
    # therefore the authoritative valuation-state handoff.
    st.session_state["dcf_valuation_assumptions_snapshot"] = {
        scenario_name: {
            key: float(value)
            for key, value in assumptions.items()
        }
        for scenario_name, assumptions in scenarios.items()
    }

    return scenarios


def get_scenario_assumptions_from_state():
    """
    Return the canonical valuation assumptions.

    Step 3 number_input keys are widget-owned. Streamlit can remove
    widget state when navigating to another wizard page, so Step 4
    must be able to fall back to the persisted non-widget snapshot.
    """
    snapshot = st.session_state.get(
        "dcf_valuation_assumptions_snapshot"
    )

    # If the live Step-3 widget keys exist, they are authoritative.
    live_keys_exist = all(
        f"dcf_scenario_{scenario}_discount_rate"
        in st.session_state
        for scenario in (
            "Worst Case",
            "Base Case",
            "Best Case",
        )
    )

    if live_keys_exist:
        assumptions = {
            "Worst Case": {
                "discount_rate": float(
                    st.session_state[
                        "dcf_scenario_Worst Case_discount_rate"
                    ]
                ),
                "terminal_growth": float(
                    st.session_state.get(
                        "dcf_scenario_Worst Case_terminal_growth",
                        0.02,
                    )
                ),
                "margin_of_safety": float(
                    st.session_state.get(
                        "dcf_scenario_Worst Case_margin_of_safety",
                        0.35,
                    )
                ),
            },
            "Base Case": {
                "discount_rate": float(
                    st.session_state[
                        "dcf_scenario_Base Case_discount_rate"
                    ]
                ),
                "terminal_growth": float(
                    st.session_state.get(
                        "dcf_scenario_Base Case_terminal_growth",
                        0.025,
                    )
                ),
                "margin_of_safety": float(
                    st.session_state.get(
                        "dcf_scenario_Base Case_margin_of_safety",
                        0.25,
                    )
                ),
            },
            "Best Case": {
                "discount_rate": float(
                    st.session_state[
                        "dcf_scenario_Best Case_discount_rate"
                    ]
                ),
                "terminal_growth": float(
                    st.session_state.get(
                        "dcf_scenario_Best Case_terminal_growth",
                        0.03,
                    )
                ),
                "margin_of_safety": float(
                    st.session_state.get(
                        "dcf_scenario_Best Case_margin_of_safety",
                        0.20,
                    )
                ),
            },
        }

        # Keep the persistent copy synchronized with edits.
        st.session_state[
            "dcf_valuation_assumptions_snapshot"
        ] = assumptions

        return assumptions

    # Step 3 widgets are no longer mounted. Use the last confirmed
    # Step-3 values rather than reverting to generic defaults.
    if snapshot:
        return snapshot

    # First-run fallback before Step 3 has ever been rendered.
    return {
        "Worst Case": {
            "discount_rate": 0.09,
            "terminal_growth": 0.02,
            "margin_of_safety": 0.35,
        },
        "Base Case": {
            "discount_rate": 0.09,
            "terminal_growth": 0.025,
            "margin_of_safety": 0.25,
        },
        "Best Case": {
            "discount_rate": 0.08,
            "terminal_growth": 0.03,
            "margin_of_safety": 0.20,
        },
    }
