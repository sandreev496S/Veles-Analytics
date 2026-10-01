from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title(
        "Company Snapshot",
        "High-level institutional profile for the selected company."
    )

    profile_col, risk_col, action_col = st.columns([2, 1, 1])

    with profile_col:
        insight_card(
            "Company Profile",
            f"{selected_company} is tracked inside the Veles neurotechnology research universe. Focus area: {selected_profile['focus']}. This workspace consolidates company profile data, funding history, technology notes, valuation outputs, and generated reports."
        )

    with risk_col:
        activity_item(
            "Risk Profile",
            selected_profile["risk"],
            "Research"
        )

    with action_col:
        activity_item(
            "Primary Action",
            "Generate valuation, create memo, or open saved model.",
            "Workspace"
        )
'''

new = '''    section_title(
        "Company Intelligence",
        "Institutional overview, research flags, and primary analyst workflow."
    )

    profile_col, signal_col = st.columns([1.5, 1])

    with profile_col:
        insight_card(
            "Institutional Profile",
            f"{selected_company} is tracked inside the Veles neurotechnology research universe. Focus area: {selected_profile['focus']}. This workspace consolidates company profile data, technology notes, competitive positioning, valuation outputs, research notes, and generated reports."
        )

        activity_item(
            "Investment Thesis Anchor",
            f"{selected_company}'s diligence profile is driven by technology modality, clinical maturity, capitalization, regulatory path, and commercial adoption risk.",
            "Research Thesis"
        )

    with signal_col:
        activity_item(
            "Risk Profile",
            selected_profile["risk"],
            "Research Flag"
        )

        activity_item(
            "Primary Workflow",
            "Open valuation history, generate reports, review notes, or compare against peer companies.",
            "Analyst Action"
        )

        activity_item(
            "Coverage Status",
            "Active monitoring inside Veles company intelligence universe.",
            "Coverage"
        )
'''

if old not in text:
    raise SystemExit("Could not find Company Snapshot block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Company Snapshot replaced with Company Intelligence.")
