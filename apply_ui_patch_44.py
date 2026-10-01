from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        competition_df = pd.DataFrame(competition_rows)

        st.dataframe(competition_df, use_container_width=True)

        activity_item(
            "Competitive Angle",
            "This table compares the selected company against the tracked BCI peer universe. Next step: add differentiation by bandwidth, invasiveness, regulatory path, and commercialization model.",
            "Analysis"
        )'''

new = '''        competition_df = pd.DataFrame(competition_rows)

        peer_col1, peer_col2, peer_col3 = st.columns(3)

        with peer_col1:
            metric_card("Peer Companies", len(competition_df), "Tracked Universe")

        with peer_col2:
            invasive_count = (competition_df["Modality"] == "Invasive").sum()
            metric_card("Invasive BCIs", invasive_count, "Peer Mix")

        with peer_col3:
            minimally_invasive_count = competition_df["Modality"].str.contains("Minimally", case=False, na=False).sum()
            metric_card("Minimally Invasive", minimally_invasive_count, "Peer Mix")

        st.dataframe(competition_df, use_container_width=True)

        activity_item(
            "Competitive Angle",
            "This table compares the selected company against the tracked BCI peer universe. Next step: add differentiation by bandwidth, invasiveness, regulatory path, and commercialization model.",
            "Analysis"
        )'''

if old not in text:
    raise SystemExit("Could not find competition dataframe block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 44 applied: Competition tab now includes summary metrics.")
