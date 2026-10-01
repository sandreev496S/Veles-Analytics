from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with competition_tab:
        activity_item(
            "Peer Set",
            "Compare against Neuralink, Synchron, Paradromics, Blackrock Neurotech, and Precision Neuroscience.",
            "Market"
        )

        activity_item(
            "Competitive Angle",
            "This will eventually summarize differentiation by bandwidth, invasiveness, regulatory path, and commercialization model.",
            "Analysis"
        )'''

new = '''    with competition_tab:
        competition_rows = []

        for peer_name, peer_profile in company_profiles.items():
            competition_rows.append({
                "Company": peer_name,
                "Stage": peer_profile["stage"],
                "Focus": peer_profile["focus"],
                "Modality": peer_profile["modality"],
                "Funding": peer_profile["funding"],
                "Valuation": peer_profile["valuation"],
                "Selected": "Yes" if peer_name == selected_company else "",
            })

        competition_df = pd.DataFrame(competition_rows)

        st.dataframe(competition_df, use_container_width=True)

        activity_item(
            "Competitive Angle",
            "This table compares the selected company against the tracked BCI peer universe. Next step: add differentiation by bandwidth, invasiveness, regulatory path, and commercialization model.",
            "Analysis"
        )'''

if old not in text:
    raise SystemExit("Could not find Competition tab block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 43 applied: Competition tab now includes peer comparison table.")
