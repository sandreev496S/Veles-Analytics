from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with funding_tab:
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
        )
'''

new = '''    with funding_tab:
        section_title(
            "Capitalization Overview",
            "Funding, valuation, financing status, and investor intelligence."
        )

        fund_k1, fund_k2, fund_k3 = st.columns(3)

        with fund_k1:
            metric_card("Known Funding", selected_profile["funding"], "Capital Raised")

        with fund_k2:
            metric_card("Valuation", selected_profile["valuation"], "Latest Known")

        with fund_k3:
            metric_card("Stage", selected_profile["stage"], "Financing Context")

        funding_left, funding_right = st.columns([1.35, 1])

        with funding_left:
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

            insight_card(
                "Capitalization Intelligence",
                f"{selected_company}'s funding profile should be interpreted through capital intensity, clinical timeline, manufacturing requirements, regulatory pathway, and ability to finance long development cycles."
            )

        with funding_right:
            activity_item(
                "Financing Signal",
                "Monitor new rounds, strategic investors, valuation resets, insider participation, and crossover investor activity.",
                "Funding"
            )

            activity_item(
                "Investor Intelligence",
                "Next step: connect investor database, round history, ownership estimates, and comparable private-market transactions.",
                "Investors"
            )

            activity_item(
                "Valuation Context",
                "Private neurotechnology valuation should be benchmarked against clinical maturity, modality risk, market size, and commercialization feasibility.",
                "Valuation"
            )
'''

if old not in text:
    raise SystemExit("Could not find current funding tab block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Research Workspace funding tab redesigned.")
