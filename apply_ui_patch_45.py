from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        st.dataframe(competition_df, use_container_width=True)

        activity_item(
            "Competitive Angle",
            "This table compares the selected company against the tracked BCI peer universe. Next step: add differentiation by bandwidth, invasiveness, regulatory path, and commercialization model.",
            "Analysis"
        )'''

new = '''        st.dataframe(competition_df, use_container_width=True)

        section_title(
            "Differentiation Matrix",
            "Early qualitative comparison across technical and commercial dimensions."
        )

        differentiation_df = pd.DataFrame([
            {
                "Dimension": "Invasiveness",
                "Selected Company": selected_profile["modality"],
                "Why It Matters": "Impacts surgical burden, adoption friction, and regulatory complexity.",
            },
            {
                "Dimension": "Technology Focus",
                "Selected Company": selected_profile["focus"],
                "Why It Matters": "Defines clinical use cases and differentiation versus peer companies.",
            },
            {
                "Dimension": "Capitalization",
                "Selected Company": selected_profile["funding"],
                "Why It Matters": "Indicates ability to fund trials, engineering, manufacturing, and commercialization.",
            },
            {
                "Dimension": "Risk Profile",
                "Selected Company": selected_profile["risk"],
                "Why It Matters": "Frames diligence priorities and valuation discount factors.",
            },
        ])

        st.dataframe(differentiation_df, use_container_width=True)

        activity_item(
            "Competitive Angle",
            "This matrix is currently qualitative. Next step: score each company by bandwidth, regulatory maturity, clinical validation, commercialization readiness, and defensibility.",
            "Analysis"
        )'''

if old not in text:
    raise SystemExit("Could not find competition dataframe and activity block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 45 applied: Competitive differentiation matrix added.")
