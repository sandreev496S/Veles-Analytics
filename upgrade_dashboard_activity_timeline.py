from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title("Recent Activity", "Latest valuation, report, and research actions.")

    activity_col, model_col = st.columns(2)

    with activity_col:
        activity_item(
            "Generated Neuralink DCF",
            "Base case intrinsic valuation model created with scenario comparison and sensitivity matrix.",
            "Valuation"
        )

        activity_item(
            "Updated Neurotech Watchlist",
            "Core BCI competitor universe refreshed for company research tracking.",
            "Workspace"
        )

    with model_col:
        activity_item(
            "Saved Biotech rNPV Model",
            "Risk-adjusted valuation model saved for future analysis and report generation.",
            "Saved Models"
        )

        activity_item(
            "Prepared Monte Carlo Output",
            "Simulation distribution and percentile table ready for analyst review.",
            "Analysis"
        )
'''

new = '''    section_title("Operational Activity", "Timeline of recent valuation, research, and reporting actions.")

    timeline_col1, timeline_col2, timeline_col3 = st.columns(3)

    with timeline_col1:
        st.markdown(
            '<div class="veles-mini-panel-title">Today</div>',
            unsafe_allow_html=True,
        )

        activity_item(
            "Generated Neuralink DCF",
            "Base case intrinsic valuation model created with scenario comparison and sensitivity matrix.",
            "Valuation"
        )

        activity_item(
            "Updated Neurotech Watchlist",
            "Core BCI competitor universe refreshed for company research tracking.",
            "Workspace"
        )

    with timeline_col2:
        st.markdown(
            '<div class="veles-mini-panel-title">Yesterday</div>',
            unsafe_allow_html=True,
        )

        activity_item(
            "Saved Biotech rNPV Model",
            "Risk-adjusted valuation model saved for future analysis and report generation.",
            "Saved Models"
        )

    with timeline_col3:
        st.markdown(
            '<div class="veles-mini-panel-title">This Week</div>',
            unsafe_allow_html=True,
        )

        activity_item(
            "Prepared Monte Carlo Output",
            "Simulation distribution and percentile table ready for analyst review.",
            "Analysis"
        )

        activity_item(
            "Report Export Ready",
            "PDF and Excel report outputs are available for saved valuation models.",
            "Reports"
        )
'''

if old not in text:
    raise SystemExit("Could not find old Recent Activity block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Dashboard activity timeline upgraded.")
