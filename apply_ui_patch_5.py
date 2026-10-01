from pathlib import Path

path = Path("app.py")
text = path.read_text()

replacements = [
    (
        '    st.markdown("##")\n\n    left, right = st.columns([2, 1])',
        '    section_title("AI Research Brief", "High-level platform intelligence and market context.")\n\n    left, right = st.columns([2, 1])',
    ),
    (
        '    st.markdown("##")\n    st.markdown("### Watchlist")',
        '    section_title("Watchlist", "Priority neurotechnology companies under active coverage.")',
    ),
    (
        '''    st.markdown("##")
    st.markdown("### Recent Activity")

    activity_col, model_col = st.columns(2)

    with activity_col:
        insight_card(
            "Recent Reports",
            "Latest generated research reports and valuation exports will appear here as the platform evolves."
        )

    with model_col:
        insight_card(
            "Latest Models",
            "Saved DCF, rNPV, and Monte Carlo models will be surfaced here for fast analyst access."
        )''',
        '''    section_title("Recent Activity", "Latest valuation, report, and research actions.")

    activity_col, model_col = st.columns(2)

    with activity_col:
        activity_item(
            "Generated Research Report",
            "A new AI-assisted company research report was created and prepared for export.",
            "Reports"
        )

        activity_item(
            "Updated Company Coverage",
            "Neurotechnology company watchlist refreshed with core BCI competitors.",
            "Workspace"
        )

    with model_col:
        activity_item(
            "Saved Valuation Model",
            "Latest DCF and rNPV models will appear here after being saved.",
            "Saved Models"
        )

        activity_item(
            "Monte Carlo Simulation",
            "Simulation outputs and probability distributions will be surfaced here.",
            "Analysis"
        )''',
    ),
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f"Could not find expected dashboard block:\n{old[:200]}")
    text = text.replace(old, new, 1)

path.write_text(text)
print("UI patch 5 applied successfully: dashboard now uses section titles and activity items.")
