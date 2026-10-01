from __future__ import annotations

import pandas as pd
import streamlit as st

from services.orchestrator.research_orchestrator import (
    build_research_dataset,
)
from services.valuation import (
    ValuationWorkspaceState,
    build_default_workspace,
    list_saved_valuations,
    load_valuation,
    run_workspace_valuation,
    save_valuation,
)


def _fmt_money(value: float | None) -> str:
    if value is None:
        return "N/A"

    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}B"

    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"

    return f"${value:,.2f}"


def _fmt_percent(value: float) -> str:
    return f"{value:.1%}"


def render_valuation_workspace() -> None:
    st.title("Valuation Workspace")
    st.caption(
        "Review observed inputs, edit analyst assumptions, "
        "and run bull/base/bear DCF scenarios."
    )

    ticker = st.text_input(
        "Ticker",
        value="RXRX",
    ).upper().strip()

    if not ticker:
        st.info("Enter a ticker.")
        return

    research = build_research_dataset(
        ticker,
        use_cache=True,
        selected_capabilities=[
            "company",
            "financials",
            "market",
            "filings",
            "company_facts",
        ],
    )

    session_key = f"valuation_workspace_{ticker}"

    if session_key not in st.session_state:
        st.session_state[session_key] = (
            build_default_workspace(research)
        )

    workspace: ValuationWorkspaceState = (
        st.session_state[session_key]
    )

    st.subheader("Observed Inputs")

    snapshot = workspace.snapshot

    observed = pd.DataFrame([
        {
            "Input": "Base Revenue",
            "Value": _fmt_money(
                snapshot["base_revenue"]["value"]
            ),
            "Status": snapshot["base_revenue"]["status"],
            "Source": snapshot["base_revenue"]["source"],
        },
        {
            "Input": "Cash",
            "Value": _fmt_money(
                snapshot["cash"]["value"]
            ),
            "Status": snapshot["cash"]["status"],
            "Source": snapshot["cash"]["source"],
        },
        {
            "Input": "Debt",
            "Value": _fmt_money(
                snapshot["debt"]["value"]
            ),
            "Status": snapshot["debt"]["status"],
            "Source": snapshot["debt"]["source"],
        },
        {
            "Input": "Beta",
            "Value": snapshot["beta"]["value"],
            "Status": snapshot["beta"]["status"],
            "Source": snapshot["beta"]["source"],
        },
        {
            "Input": "Diluted Shares",
            "Value": (
                f"{snapshot['diluted_shares_outstanding']['value']:,.0f}"
                if snapshot[
                    "diluted_shares_outstanding"
                ]["value"] is not None
                else "N/A"
            ),
            "Status": snapshot[
                "diluted_shares_outstanding"
            ]["status"],
            "Source": snapshot[
                "diluted_shares_outstanding"
            ]["source"],
        },
    ])

    st.dataframe(
        observed,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Forecast Assumptions")

    forecast_df = pd.DataFrame({
        "Year": [
            snapshot["base_year"] + index
            for index in range(1, 6)
        ],
        "Revenue Growth": workspace.forecast_profile[
            "revenue_growth_rates"
        ],
        "EBIT Margin": workspace.forecast_profile[
            "ebit_margins"
        ],
    })

    edited_forecast = st.data_editor(
        forecast_df,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        column_config={
            "Year": st.column_config.NumberColumn(
                disabled=True,
            ),
            "Revenue Growth": st.column_config.NumberColumn(
                format="%.1f%%",
                step=0.01,
            ),
            "EBIT Margin": st.column_config.NumberColumn(
                format="%.1f%%",
                step=0.05,
            ),
        },
    )

    workspace.forecast_profile[
        "revenue_growth_rates"
    ] = edited_forecast[
        "Revenue Growth"
    ].tolist()

    workspace.forecast_profile[
        "ebit_margins"
    ] = edited_forecast[
        "EBIT Margin"
    ].tolist()

    col1, col2, col3 = st.columns(3)

    with col1:
        workspace.forecast_profile["tax_rate"] = st.number_input(
            "Tax Rate",
            value=float(
                workspace.forecast_profile["tax_rate"]
            ),
            step=0.01,
            format="%.3f",
        )

        workspace.forecast_profile[
            "terminal_growth_rate"
        ] = st.number_input(
            "Terminal Growth Rate",
            value=float(
                workspace.forecast_profile[
                    "terminal_growth_rate"
                ]
            ),
            step=0.005,
            format="%.3f",
        )

    with col2:
        workspace.forecast_profile[
            "depreciation_amortization_pct_revenue"
        ] = st.number_input(
            "D&A as % Revenue",
            value=float(
                workspace.forecast_profile[
                    "depreciation_amortization_pct_revenue"
                ]
            ),
            step=0.01,
            format="%.3f",
        )

        workspace.forecast_profile[
            "capex_pct_revenue"
        ] = st.number_input(
            "CapEx as % Revenue",
            value=float(
                workspace.forecast_profile[
                    "capex_pct_revenue"
                ]
            ),
            step=0.01,
            format="%.3f",
        )

    with col3:
        workspace.forecast_profile[
            "nwc_pct_revenue_change"
        ] = st.number_input(
            "NWC as % Revenue Change",
            value=float(
                workspace.forecast_profile[
                    "nwc_pct_revenue_change"
                ]
            ),
            step=0.01,
            format="%.3f",
        )

    st.subheader("Capital Market Assumptions")

    c1, c2, c3 = st.columns(3)

    with c1:
        workspace.capital_market_assumptions[
            "risk_free_rate"
        ] = st.number_input(
            "Risk-Free Rate",
            value=float(
                workspace.capital_market_assumptions[
                    "risk_free_rate"
                ]
            ),
            step=0.005,
            format="%.3f",
        )

        workspace.capital_market_assumptions[
            "equity_risk_premium"
        ] = st.number_input(
            "Equity Risk Premium",
            value=float(
                workspace.capital_market_assumptions[
                    "equity_risk_premium"
                ]
            ),
            step=0.005,
            format="%.3f",
        )

    with c2:
        workspace.capital_market_assumptions[
            "cost_of_debt"
        ] = st.number_input(
            "Pre-Tax Cost of Debt",
            value=float(
                workspace.capital_market_assumptions[
                    "cost_of_debt"
                ]
            ),
            step=0.005,
            format="%.3f",
        )

        beta_override = st.number_input(
            "Beta Override (0 = use observed)",
            value=float(
                workspace.capital_market_assumptions[
                    "beta_override"
                ] or 0.0
            ),
            step=0.05,
            format="%.2f",
        )

        workspace.capital_market_assumptions[
            "beta_override"
        ] = (
            beta_override
            if beta_override > 0
            else None
        )

    with c3:
        debt_weight = st.number_input(
            "Debt Weight",
            value=float(
                workspace.capital_market_assumptions[
                    "debt_weight"
                ]
            ),
            step=0.01,
            format="%.3f",
        )

        workspace.capital_market_assumptions[
            "debt_weight"
        ] = debt_weight

        workspace.capital_market_assumptions[
            "equity_weight"
        ] = 1.0 - debt_weight

        st.metric(
            "Equity Weight",
            _fmt_percent(1.0 - debt_weight),
        )

    st.session_state[session_key] = workspace

    if st.button(
        "Run DCF Valuation",
        type="primary",
        use_container_width=True,
    ):
        with st.spinner("Running valuation..."):
            workspace = run_workspace_valuation(
                research,
                workspace,
            )

            st.session_state[session_key] = workspace

    if workspace.errors:
        for error in workspace.errors:
            st.error(error)

    st.subheader("Saved Valuations")

    saved_models = list_saved_valuations(ticker)

    if saved_models:
        saved_options = {
            (
                f"{item['name']} | "
                f"{item.get('saved_at', 'Unknown date')}"
            ): item["path"]
            for item in saved_models
        }

        selected_saved_label = st.selectbox(
            "Load saved model",
            options=list(saved_options.keys()),
            key=f"saved_valuation_selector_{ticker}",
        )

        if st.button(
            "Load Selected Valuation",
            key=f"load_saved_valuation_{ticker}",
            use_container_width=True,
        ):
            saved = load_valuation(
                saved_options[selected_saved_label]
            )

            workspace.result = saved["payload"]
            workspace.errors = []

            st.session_state[session_key] = workspace
            st.success("Saved valuation loaded.")

    else:
        st.caption(
            "No saved valuation models exist for this ticker."
        )

    if workspace.result:
        save_name = st.text_input(
            "Valuation model name",
            value="Base DCF",
            key=f"valuation_save_name_{ticker}",
        )

        if st.button(
            "Save Current Valuation",
            key=f"save_current_valuation_{ticker}",
            use_container_width=True,
        ):
            saved_path = save_valuation(
                ticker=ticker,
                payload=workspace.result,
                name=save_name,
            )

            st.success(
                f"Valuation saved: {saved_path}"
            )

    if not workspace.result:
        return

    result = workspace.result
    base = result["base_result"]
    scenarios = result["scenarios"]

    st.subheader("Valuation Summary")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric(
        "Implied Value / Share",
        f"${base['implied_value_per_share']:,.2f}",
    )
    m2.metric(
        "Enterprise Value",
        _fmt_money(base["enterprise_value"]),
    )
    m3.metric(
        "Equity Value",
        _fmt_money(base["equity_value"]),
    )
    m4.metric(
        "WACC",
        _fmt_percent(base["wacc"]),
    )

    scenario_df = pd.DataFrame([
        {
            "Scenario": name.title(),
            "Value / Share": scenario[
                "implied_value_per_share"
            ],
            "Enterprise Value": scenario[
                "enterprise_value"
            ],
            "Equity Value": scenario[
                "equity_value"
            ],
        }
        for name, scenario in scenarios.items()
    ])

    st.dataframe(
        scenario_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Value / Share": st.column_config.NumberColumn(
                format="$%.2f",
            ),
            "Enterprise Value": st.column_config.NumberColumn(
                format="$%.0f",
            ),
            "Equity Value": st.column_config.NumberColumn(
                format="$%.0f",
            ),
        },
    )

    forecast = pd.DataFrame(
        base["forecast"]
    )

    st.subheader("Forecast Output")

    st.dataframe(
        forecast[
            [
                "year",
                "revenue",
                "revenue_growth",
                "ebit_margin",
                "ebit",
                "unlevered_fcf",
                "present_value_fcf",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    sensitivity = result.get("sensitivity")

    if sensitivity:
        st.subheader("DCF Sensitivity")

        matrix = pd.DataFrame(
            index=[
                f"{value:.1%}"
                for value in sensitivity[
                    "wacc_values"
                ]
            ],
            columns=[
                f"{value:.1%}"
                for value in sensitivity[
                    "terminal_growth_values"
                ]
            ],
            dtype=float,
        )

        for cell in sensitivity["cells"]:
            matrix.loc[
                f"{cell['wacc']:.1%}",
                f"{cell['terminal_growth_rate']:.1%}",
            ] = cell["implied_value_per_share"]

        st.dataframe(
            matrix.style.format("${:,.2f}"),
            use_container_width=True,
        )

    warnings = result[
        "assumption_build"
    ].get(
        "warnings",
        [],
    )

    if warnings:
        st.subheader("Warnings")

        for warning in warnings:
            st.warning(warning)
