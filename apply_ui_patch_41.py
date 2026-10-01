from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with funding_tab:
        metric_card("Known Funding", selected_profile["funding"], selected_profile["stage"])

        activity_item(
            "Funding History",
            "Rounds, investors, implied valuation, and financing history will be stored here.",
            "Company Data"
        )'''

new = '''    with funding_tab:
        metric_card("Known Funding", selected_profile["funding"], selected_profile["stage"])

        funding_history = pd.DataFrame([
            {
                "Company": selected_company,
                "Stage": selected_profile["stage"],
                "Known Funding": selected_profile["funding"],
                "Latest Known Valuation": selected_profile["valuation"],
                "Status": "Tracked",
            }
        ])

        st.dataframe(funding_history, use_container_width=True)

        activity_item(
            "Funding History",
            "This table is currently seeded from the company profile map. Next step: connect it to a persistent companies/funding database.",
            "Company Data"
        )'''

if old not in text:
    raise SystemExit("Could not find Funding tab block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 41 applied: Funding tab now includes a company funding table.")
