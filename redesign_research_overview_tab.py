from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with overview_tab:
        insight_card(
            "Overview",
            f"{selected_company} is monitored as part of the Veles neurotechnology research universe. Focus area: {selected_profile['focus']}."
        )

        activity_item(
            "Current Coverage View",
            "This section will become the main institutional company profile, combining fundamentals, technology, funding, risk, and valuation context.",
            "Overview"
        )
'''

new = '''    with overview_tab:
        section_title(
            "Company Overview",
            "Institutional summary, thesis, risks, and recent developments."
        )

        overview_left, overview_right = st.columns([1.35, 1])

        with overview_left:
            insight_card(
                "Business Summary",
                f"{selected_company} is monitored as part of the Veles neurotechnology research universe. Focus area: {selected_profile['focus']}. The company profile should be evaluated through technology defensibility, clinical maturity, capitalization, regulatory pathway, and commercialization potential."
            )

            insight_card(
                "Investment Thesis",
                f"The investment case for {selected_company} depends on whether its technology modality can support durable clinical utility, scalable deployment, defensible data infrastructure, and a credible path toward reimbursement or strategic acquisition."
            )

        with overview_right:
            activity_item(
                "Technology Profile",
                f"{selected_profile['modality']} · {selected_profile['focus']}",
                "Technical Lens"
            )

            activity_item(
                "Primary Risk",
                selected_profile["risk"],
                "Risk Flag"
            )

            activity_item(
                "Recent Developments",
                "Track financing updates, trial progress, regulatory movement, product milestones, partnerships, and leadership changes.",
                "Monitoring"
            )
'''

if old not in text:
    raise SystemExit("Could not find current overview tab block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Research Workspace overview tab redesigned.")
