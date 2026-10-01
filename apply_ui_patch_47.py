from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        scoring_df = pd.DataFrame([
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

        st.dataframe(scoring_df, use_container_width=True)'''

new = '''        scoring_df = pd.DataFrame([
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

        selected_score = scoring_df.loc[
            scoring_df["Company"] == selected_company,
            "Overall Score"
        ].iloc[0]

        average_score = scoring_df["Overall Score"].mean()

        score_col1, score_col2, score_col3 = st.columns(3)

        with score_col1:
            metric_card("Selected Score", f"{selected_score}/10", selected_company)

        with score_col2:
            metric_card("Peer Average", f"{average_score:.1f}/10", "Tracked Universe")

        with score_col3:
            metric_card("Coverage Depth", len(scoring_df), "Companies Scored")

        st.dataframe(scoring_df, use_container_width=True)'''

if old not in text:
    raise SystemExit("Could not find scoring dataframe block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 47 applied: competitive score metrics added.")
