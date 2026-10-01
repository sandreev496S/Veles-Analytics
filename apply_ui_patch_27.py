from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title(
        "Research Modules",
        "Company profile, funding, technology, competition, valuation history, notes, and reports."
    )

    module_col1, module_col2, module_col3 = st.columns(3)

    with module_col1:
        activity_item(
            "Funding",
            "Rounds, investors, implied valuation, and financing history.",
            "Company Data"
        )

        activity_item(
            "Technology",
            "Device type, modality, invasiveness, patents, and research papers.",
            "Technical"
        )

    with module_col2:
        activity_item(
            "Competition",
            "Peer comparison against implantable and non-invasive BCI companies.",
            "Market"
        )

        activity_item(
            "Valuation History",
            "Saved DCF, rNPV, and Monte Carlo models linked to this company.",
            "Models"
        )

    with module_col3:
        activity_item(
            "Research Notes",
            "Analyst notes, thesis updates, risks, catalysts, and diligence questions.",
            "Notes"
        )

        activity_item(
            "Reports",
            "Generated PDFs, Excel models, and AI investment memos.",
            "Exports"
        )'''

new = '''    section_title(
        "Company Terminal",
        "Overview, funding, technology, competition, valuation history, notes, and reports."
    )

    overview_tab, funding_tab, tech_tab, competition_tab, valuation_tab, notes_tab, reports_tab = st.tabs(
        [
            "Overview",
            "Funding",
            "Technology",
            "Competition",
            "Valuation History",
            "Notes",
            "Reports",
        ]
    )

    with overview_tab:
        insight_card(
            "Overview",
            f"{selected_company} is monitored as part of the Veles neurotechnology research universe. Focus area: {selected_profile['focus']}."
        )

        activity_item(
            "Current Coverage View",
            "This section will become the main institutional company profile, combining fundamentals, technology, funding, risk, and valuation context.",
            "Overview"
        )

    with funding_tab:
        metric_card("Known Funding", selected_profile["funding"], selected_profile["stage"])

        activity_item(
            "Funding History",
            "Rounds, investors, implied valuation, and financing history will be stored here.",
            "Company Data"
        )

    with tech_tab:
        metric_card("Modality", selected_profile["modality"], selected_profile["focus"])

        activity_item(
            "Technology Profile",
            "Device type, invasiveness, patents, technical differentiation, and relevant research papers will be organized here.",
            "Technical"
        )

    with competition_tab:
        activity_item(
            "Peer Set",
            "Compare against Neuralink, Synchron, Paradromics, Blackrock Neurotech, and Precision Neuroscience.",
            "Market"
        )

        activity_item(
            "Competitive Angle",
            "This will eventually summarize differentiation by bandwidth, invasiveness, regulatory path, and commercialization model.",
            "Analysis"
        )

    with valuation_tab:
        activity_item(
            "Valuation History",
            "Saved DCF, rNPV, and Monte Carlo models linked to this company will appear here.",
            "Models"
        )

        activity_item(
            "Next Step",
            "Connect saved valuation records to selected_company so this tab becomes dynamic.",
            "Planned"
        )

    with notes_tab:
        activity_item(
            "Research Notes",
            "Analyst notes, thesis updates, risks, catalysts, and diligence questions will live here.",
            "Notes"
        )

    with reports_tab:
        activity_item(
            "Reports",
            "Generated PDFs, Excel models, and AI investment memos linked to this company will appear here.",
            "Exports"
        )'''

if old not in text:
    raise SystemExit("Could not find Research Modules block. Need to inspect a wider range.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 27 applied: Research Workspace now has company terminal tabs.")
