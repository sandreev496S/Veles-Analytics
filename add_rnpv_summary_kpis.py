from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        st.info(f"Clinical / regulatory stage: {clinical_stage} | Probability of approval: {probability_of_approval:.1%}")

        st.dataframe(
            pd.DataFrame(
                rnpv_valuation.items(),
                columns=["Metric", "Value"],
            ),
            use_container_width=True,
        )'''

new = '''        st.info(f"Clinical / regulatory stage: {clinical_stage} | Probability of approval: {probability_of_approval:.1%}")

        rnpv_valuation_df = pd.DataFrame(
            rnpv_valuation.items(),
            columns=["Metric", "Value"],
        )

        rnpv_lookup = dict(rnpv_valuation)

        rnpv_kpi1, rnpv_kpi2, rnpv_kpi3, rnpv_kpi4 = st.columns(4)

        with rnpv_kpi1:
            metric_card(
                "Enterprise Value",
                rnpv_lookup.get("Enterprise Value ($M)", rnpv_lookup.get("Risk-Adjusted Enterprise Value ($M)", "—")),
                "rNPV Output"
            )

        with rnpv_kpi2:
            metric_card(
                "Equity Value",
                rnpv_lookup.get("Equity Value ($M)", "—"),
                "After Cash / Debt"
            )

        with rnpv_kpi3:
            metric_card(
                "Implied Share Price",
                rnpv_lookup.get("Implied Share Price ($)", "—"),
                "Per Share"
            )

        with rnpv_kpi4:
            metric_card(
                "Approval Probability",
                f"{probability_of_approval:.1%}",
                clinical_stage
            )

        st.dataframe(rnpv_valuation_df, use_container_width=True)'''

if old not in text:
    raise SystemExit("Could not find rNPV summary dataframe block.")

text = text.replace(old, new, 1)
path.write_text(text)
print("rNPV KPI summary added.")
