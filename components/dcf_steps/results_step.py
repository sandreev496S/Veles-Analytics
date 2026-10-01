import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from components.ui.cards import kpi_card
from components.ui.panels import section_panel
from services.pdf_report import create_dcf_pdf
from services.excel_export import create_standard_dcf_excel


def render_results_step(section_title, metric_card, activity_item):
    outputs = st.session_state.get("standard_dcf_outputs") or st.session_state.get("dcf_outputs")

    section_title(
        "Step 5 — Valuation Results",
        "Review intrinsic value, scenario outputs, sensitivity analysis, comparables, charts, and exports."
    )

    if not outputs:
        activity_item(
            "No DCF Results Yet",
            "Go to Step 4 and run the model to generate valuation outputs.",
            "Results"
        )
        return

    company_name = outputs.get("company_name")
    current_market_cap = outputs.get("current_market_cap")
    starting_revenue = outputs.get("starting_revenue")
    forecast_years = outputs.get("forecast_years")
    scenarios = outputs.get("scenarios")

    cash = outputs.get("cash", 0.0)
    debt = outputs.get("debt", 0.0)
    shares = outputs.get("shares", 0.0)

    summary_df = outputs.get("summary_df")
    base_forecast = outputs.get("base_forecast")
    sens_df = outputs.get("sens_df")
    comps_df = outputs.get("comps_df")
    comps_summary = outputs.get("comps_summary")
    comps_summary_df = outputs.get("comps_summary_df")
    valuation_crosscheck_df = outputs.get("valuation_crosscheck_df")
    implied_growth = outputs.get("implied_growth")

    if summary_df is not None and not summary_df.empty:
        base_case = summary_df.loc[
            summary_df["Scenario"] == "Base Case"
        ].iloc[0]

        upside_pct = (
            base_case["Equity Value ($M)"] / current_market_cap - 1
            if current_market_cap else 0
        )

        result_col1, result_col2, result_col3, result_col4 = st.columns(4)

        with result_col1:
            kpi_card(
                "Implied Share Price",
                f"${base_case['Implied Share Price ($)']:.2f}",
                "Base Case"
            )

        with result_col2:
            kpi_card(
                "Equity Value",
                f"${base_case['Equity Value ($M)']:,.0f}M",
                "DCF Output"
            )

        with result_col3:
            kpi_card(
                "Upside / Downside",
                f"{upside_pct:.1%}",
                "vs. Current Market Cap",
                positive=upside_pct >= 0
            )

        with result_col4:
            kpi_card(
                "MoS Price",
                f"${base_case['MoS Price ($)']:.2f}",
                "Margin of Safety"
            )

        base_wacc = st.session_state.get("dcf_scenario_Base Case_discount_rate")
        wacc_cost_of_equity = st.session_state.get("wacc_cost_of_equity")
        wacc_after_tax_debt = st.session_state.get("wacc_after_tax_cost_of_debt")

        if base_wacc is not None:
            section_panel(
                "Discount Rate Source",
                "Base Case discount rate currently linked to the DCF valuation."
            )

            wacc_col1, wacc_col2, wacc_col3 = st.columns(3)

            with wacc_col1:
                metric_card(
                    "Base Case WACC",
                    f"{base_wacc:.1%}",
                    "Discount Rate"
                )

            with wacc_col2:
                metric_card(
                    "Cost of Equity",
                    f"{wacc_cost_of_equity:.1%}" if wacc_cost_of_equity is not None else "—",
                    "CAPM Output"
                )

            with wacc_col3:
                metric_card(
                    "After-Tax Debt Cost",
                    f"{wacc_after_tax_debt:.1%}" if wacc_after_tax_debt is not None else "—",
                    "Debt Cost"
                )

        with st.expander("Scenario Output", expanded=False):
            st.caption("Compare downside, base case, and upside valuation outcomes.")
            st.dataframe(summary_df, use_container_width=True)

    if base_forecast is not None and not base_forecast.empty:
        with st.expander("Base Case Operating Forecast", expanded=False):
            st.caption("Revenue and free cash flow forecast for the base case.")
            st.dataframe(base_forecast, use_container_width=True)

    if sens_df is not None and not sens_df.empty:
        section_panel(
            "Sensitivity Matrix",
            "Base case implied share price sensitivity."
        )

        with st.expander("Sensitivity Matrix", expanded=False):
            st.dataframe(sens_df, use_container_width=True)

        sens_heatmap = px.imshow(
            sens_df.astype(float),
            text_auto=".2f",
            aspect="auto",
            title="Sensitivity Heatmap — Implied Share Price",
        )

        sens_heatmap.update_layout(
            xaxis_title="Terminal Growth",
            yaxis_title="Discount Rate",
            height=320,
            margin=dict(l=20, r=20, t=40, b=20),
        )

        with st.expander("Sensitivity Heatmap", expanded=False):
            st.plotly_chart(
                sens_heatmap,
                use_container_width=True,
                key="dcf_sensitivity_heatmap_compact",
            )

    if implied_growth is not None:
        section_panel(
            "Reverse DCF — Implied Growth",
            "Revenue growth implied by the current market capitalization."
        )

        st.metric("Implied Annual Revenue Growth", f"{implied_growth:.2%}")

    if comps_summary:
        section_panel(
            "Comparable Company Valuation",
            "Current/LTM trading multiples using operating peers for valuation and nuclear peers as contextual references."
        )

        def _fmt_multiple(value):
            try:
                if value is None or pd.isna(value):
                    return "—"
                return f"{float(value):.1f}x"
            except Exception:
                return "—"

        comp_col1, comp_col2, comp_col3 = st.columns(3)

        with comp_col1:
            metric_card(
                "Core Median EV / Revenue",
                _fmt_multiple(comps_summary.get("Median EV/Revenue")),
                "Operating Peer Set"
            )

        with comp_col2:
            metric_card(
                "Core Median EV / EBITDA",
                _fmt_multiple(comps_summary.get("Median EV/EBITDA")),
                "Operating Peer Set"
            )

        with comp_col3:
            metric_card(
                "Core Median P / E",
                _fmt_multiple(comps_summary.get("Median P/E")),
                "Operating Peer Set"
            )

        core_count = int(comps_summary.get("Core Peer Count", 0) or 0)
        reference_count = int(
            comps_summary.get("Reference Peer Count", 0) or 0
        )

        st.caption(
            f"Primary valuation uses {core_count} operating peers. "
            f"{reference_count} nuclear/reference peers remain in the "
            "table for sector context but do not determine the primary median."
        )

        valuation_cards = [
            (
                "Revenue Multiple",
                comps_summary.get(
                    "Implied Share Price from Revenue ($)"
                ),
                "EV / Revenue",
            ),
            (
                "EBITDA Multiple",
                comps_summary.get(
                    "Implied Share Price from EBITDA ($)"
                ),
                "EV / EBITDA",
            ),
            (
                "Earnings Multiple",
                comps_summary.get(
                    "Implied Share Price from P/E ($)"
                ),
                "P / E",
            ),
        ]

        val_col1, val_col2, val_col3 = st.columns(3)

        for col, (title, value, subtitle) in zip(
            [val_col1, val_col2, val_col3],
            valuation_cards,
        ):
            with col:
                metric_card(
                    title,
                    (
                        f"${float(value):.2f}"
                        if value is not None and not pd.isna(value)
                        else "—"
                    ),
                    subtitle,
                )

    if comps_df is not None and not comps_df.empty:
        display_columns = [
            "Company",
            "Ticker",
            "Peer Type",
            "Revenue Growth",
            "EBITDA Margin",
            "EV/Revenue",
            "EV/EBITDA",
            "P/E",
        ]

        available_columns = [
            c for c in display_columns
            if c in comps_df.columns
        ]

        comps_display = comps_df[available_columns].copy()

        if "Peer Type" in comps_display.columns:
            target_mask = (
                comps_display["Peer Type"]
                .astype(str)
                .eq("Target Company")
            )

            if target_mask.any():
                target_rows = comps_display.loc[target_mask]
                peer_rows = comps_display.loc[~target_mask]

                comps_display = pd.concat(
                    [target_rows, peer_rows],
                    ignore_index=True,
                )

        if "Revenue Growth" in comps_display.columns:
            comps_display["Revenue Growth"] = comps_display[
                "Revenue Growth"
            ].map(
                lambda x: (
                    f"{float(x):.1%}"
                    if x is not None and not pd.isna(x)
                    else "—"
                )
            )

        if "EBITDA Margin" in comps_display.columns:
            comps_display["EBITDA Margin"] = comps_display[
                "EBITDA Margin"
            ].map(
                lambda x: (
                    f"{float(x):.1%}"
                    if x is not None and not pd.isna(x)
                    else "—"
                )
            )

        for multiple_col in [
            "EV/Revenue",
            "EV/EBITDA",
            "P/E",
        ]:
            if multiple_col in comps_display.columns:
                comps_display[multiple_col] = comps_display[
                    multiple_col
                ].map(
                    lambda x: (
                        f"{float(x):.2f}x"
                        if x is not None and not pd.isna(x)
                        else "—"
                    )
                )

        with st.expander(
            "Comparable Companies Table",
            expanded=True,
        ):
            st.dataframe(
                comps_display,
                use_container_width=True,
                hide_index=True,
            )

        if "Rationale" in comps_df.columns:
            with st.expander(
                "Peer Selection Rationale",
                expanded=False,
            ):
                rationale_cols = [
                    c for c in [
                        "Company",
                        "Ticker",
                        "Peer Type",
                        "Rationale",
                    ]
                    if c in comps_df.columns
                ]

                st.dataframe(
                    comps_df[rationale_cols],
                    use_container_width=True,
                    hide_index=True,
                )

    if comps_summary_df is not None and not comps_summary_df.empty:
        with st.expander(
            "Comparable Valuation Detail",
            expanded=False,
        ):
            st.dataframe(
                comps_summary_df,
                use_container_width=True,
                hide_index=True,
            )

    if (
        valuation_crosscheck_df is not None
        and not valuation_crosscheck_df.empty
    ):
        section_panel(
            "Valuation Cross-Check",
            "Side-by-side comparison of intrinsic DCF value and current/LTM trading-comparable outputs."
        )

        crosscheck_display = valuation_crosscheck_df.copy()

        if "Implied Share Price ($)" in crosscheck_display.columns:
            crosscheck_display["Implied Share Price ($)"] = (
                crosscheck_display["Implied Share Price ($)"]
                .map(
                    lambda x: (
                        f"${float(x):.2f}"
                        if x is not None and not pd.isna(x)
                        else "—"
                    )
                )
            )

        st.dataframe(
            crosscheck_display,
            use_container_width=True,
            hide_index=True,
        )

    if base_forecast is not None and not base_forecast.empty:
        with st.expander("Forecast Charts", expanded=False):
            st.caption("Compact view of revenue and free cash flow trajectory.")

            chart_col1, chart_col2 = st.columns(2)

            revenue_chart = px.line(
                base_forecast,
                x="Year",
                y="Revenue ($M)",
                markers=True,
                title="Revenue Forecast",
            )
            revenue_chart.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
            )

            with chart_col1:
                st.plotly_chart(
                    revenue_chart,
                    use_container_width=True,
                    key="dcf_revenue_chart_compact",
                )

            fcf_chart = px.line(
                base_forecast,
                x="Year",
                y="FCFF ($M)",
                markers=True,
                title="Free Cash Flow Forecast",
            )
            fcf_chart.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
            )

            with chart_col2:
                st.plotly_chart(
                    fcf_chart,
                    use_container_width=True,
                    key="dcf_fcf_chart_compact",
                )

        if summary_df is not None and scenarios:
            base_case_ev = summary_df.loc[
                summary_df["Scenario"] == "Base Case",
                "Enterprise Value ($M)",
            ].iloc[0]

            pv_fcf = base_forecast["PV FCFF ($M)"].sum()
            pv_terminal = base_case_ev - pv_fcf

            waterfall = go.Figure(
                go.Waterfall(
                    name="DCF Waterfall",
                    orientation="v",
                    measure=["relative", "relative", "total"],
                    x=["PV Forecast FCFF", "PV Terminal Value", "Enterprise Value"],
                    y=[
                        pv_fcf,
                        pv_terminal,
                        base_case_ev,
                    ],
                )
            )

            waterfall.update_layout(
                title="Enterprise Value Waterfall",
                yaxis_title="$M",
                height=320,
                margin=dict(l=20, r=20, t=40, b=20),
            )

            with st.expander("Enterprise Value Bridge", expanded=False):
                st.plotly_chart(
                    waterfall,
                    use_container_width=True,
                    key="dcf_ev_waterfall_compact",
                )

    if summary_df is not None and base_forecast is not None and sens_df is not None and comps_df is not None and comps_summary_df is not None:
        pdf_bytes = create_dcf_pdf(
            company_name=company_name,
            summary_df=summary_df,
            forecast_df=base_forecast,
            sensitivity_df=sens_df,
            comps_df=comps_df,
            comps_summary_df=comps_summary_df,
            valuation_crosscheck_df=valuation_crosscheck_df,
        )

        st.session_state.setdefault("standard_dcf_outputs", {})["pdf"] = pdf_bytes

        # Excel receives the SAME state that produced Step 5.
        # This prevents the exporter from rebuilding a second DCF.
        company_inputs_for_export = {
            "starting_revenue": starting_revenue,
            "current_market_cap": current_market_cap,
            "cash": cash,
            "debt": debt,
            "shares": shares,
        }

        # Use the WACC assumptions frozen into the completed model run.
        # Do not reconstruct these from widget state on Step 5.
        wacc_inputs_for_export = dict(
            outputs.get("wacc_inputs")
            or st.session_state.get("dcf_wacc_inputs_snapshot")
            or {}
        )

        standard_excel = create_standard_dcf_excel(
            company_name=company_name,
            summary_df=summary_df,
            forecast_df=base_forecast,
            sensitivity_df=sens_df,
            comps_df=comps_df,
            comps_summary_df=comps_summary_df,
            valuation_crosscheck_df=valuation_crosscheck_df,
            scenarios=scenarios,
            company_inputs=company_inputs_for_export,
            wacc_inputs=wacc_inputs_for_export,
        )

        st.session_state.setdefault("standard_dcf_outputs", {})["standard_excel"] = standard_excel

        # Exports are generated here and displayed in the Standard DCF Action Center.
