from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        summary_df = pd.DataFrame(summary_rows)

        st.subheader("Scenario Comparison")
        st.dataframe(summary_df, use_container_width=True)'''

new = '''        summary_df = pd.DataFrame(summary_rows)

        base_case_row = summary_df.loc[
            summary_df["Scenario"] == "Base Case"
        ].iloc[0]

        upside_pct = (
            base_case_row["Equity Value ($M)"] / current_market_cap - 1
            if current_market_cap else 0
        )

        section_title(
            "Step 4 — Executive Summary",
            "Base case valuation conclusion and headline investment view."
        )

        result_col1, result_col2, result_col3, result_col4 = st.columns(4)

        with result_col1:
            metric_card(
                "Implied Share Price",
                f"${base_case_row['Implied Share Price ($)']:.2f}",
                "Base Case"
            )

        with result_col2:
            metric_card(
                "Equity Value",
                f"${base_case_row['Equity Value ($M)']:,.0f}M",
                "DCF Output"
            )

        with result_col3:
            metric_card(
                "Upside / Downside",
                f"{upside_pct:.1%}",
                "vs. Current Market Cap",
                positive=upside_pct >= 0
            )

        with result_col4:
            metric_card(
                "MoS Price",
                f"${base_case_row['MoS Price ($)']:.2f}",
                "Margin of Safety"
            )

        section_title(
            "Scenario Comparison",
            "Compare downside, base case, and upside valuation outcomes."
        )

        st.dataframe(summary_df, use_container_width=True)'''

if old not in text:
    raise SystemExit("Could not find Standard DCF summary output block.")

text = text.replace(old, new, 1)

path.write_text(text)
print("UI patch 10 applied successfully: Standard DCF executive summary cards added.")
