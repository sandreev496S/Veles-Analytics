from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        st.dataframe(comps_df, use_container_width=True)
        comps_summary_df = pd.DataFrame(comps_summary.items(), columns=["Metric", "Value"])

        st.dataframe(
            comps_summary_df,
            use_container_width=True,
        )'''

new = '''        comps_summary_df = pd.DataFrame(comps_summary.items(), columns=["Metric", "Value"])

        section_title(
            "Comparable Valuation",
            "Peer-derived valuation multiples and implied enterprise value outputs."
        )

        comp_col1, comp_col2, comp_col3 = st.columns(3)

        with comp_col1:
            metric_card(
                "Median EV / Revenue",
                f"{comps_summary['Median EV/Revenue']:.1f}x",
                "Peer Set"
            )

        with comp_col2:
            metric_card(
                "Median EV / EBITDA",
                f"{comps_summary['Median EV/EBITDA']:.1f}x",
                "Peer Set"
            )

        with comp_col3:
            metric_card(
                "Median P / E",
                f"{comps_summary['Median P/E']:.1f}x",
                "Peer Set"
            )

        st.dataframe(comps_df, use_container_width=True)

        st.dataframe(
            comps_summary_df,
            use_container_width=True,
        )'''

if old not in text:
    raise SystemExit("Could not find comparable valuation block.")

text = text.replace(old, new, 1)

path.write_text(text)
print("UI patch 12 applied successfully: comparable valuation cards added.")
