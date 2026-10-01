from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with right:
        company_card(
            "Neuralink",
            "Series D",
            "$6.1B valuation"
        )

elif page == "Standard DCF":'''

new = '''    with right:
        company_card(
            "Neuralink",
            "Series D",
            "$6.1B valuation"
        )

    st.markdown("##")
    st.markdown("### Watchlist")

    w1, w2, w3, w4, w5 = st.columns(5)

    with w1:
        company_card("Neuralink", "Series D", "$6.1B valuation")

    with w2:
        company_card("Synchron", "Series C", "Private valuation")

    with w3:
        company_card("Paradromics", "Clinical-stage", "Private valuation")

    with w4:
        company_card("Blackrock Neurotech", "Growth stage", "Private valuation")

    with w5:
        company_card("Precision Neuroscience", "Series B", "Private valuation")

    st.markdown("##")
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
        )

elif page == "Standard DCF":'''

if old not in text:
    raise SystemExit("Could not find dashboard insertion point. Patch 3 not applied.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 3 applied successfully: dashboard watchlist and activity sections added.")
