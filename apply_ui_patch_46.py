from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        st.dataframe(differentiation_df, use_container_width=True)

        activity_item(
            "Competitive Angle",
            "This matrix is currently qualitative. Next step: score each company by bandwidth, regulatory maturity, clinical validation, commercialization readiness, and defensibility.",
            "Analysis"
        )'''

new = '''        st.dataframe(differentiation_df, use_container_width=True)

        section_title(
            "Competitive Scoring Model",
            "Early qualitative scorecard for market and technology positioning."
        )

        scoring_df = pd.DataFrame([
            {
                "Company": peer_name,
                "Technology Differentiation": 8 if peer_name == selected_company else 7,
                "Clinical Maturity": 7 if "Clinical" in peer_profile["stage"] else 6,
                "Capitalization": 8 if "$" in peer_profile["funding"] else 5,
                "Regulatory Risk": 6,
                "Overall Score": 7,
            }
            for peer_name, peer_profile in company_profiles.items()
        ])

        st.dataframe(scoring_df, use_container_width=True)

        activity_item(
            "Competitive Angle",
            "This scorecard is a first-pass qualitative model. Next step: replace static scores with analyst inputs and stored company-level research data.",
            "Analysis"
        )'''

if old not in text:
    raise SystemExit("Could not find differentiation matrix block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 46 applied: competitive scoring model added.")
