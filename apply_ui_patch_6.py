from pathlib import Path

path = Path("app.py")
text = path.read_text()

old_nav = '''        "Dashboard",
        "Standard DCF",
        "Biotech rNPV",
        "Saved Valuations",
        "Saved Reports",
        "Methodology",'''

new_nav = '''        "Dashboard",
        "Research Workspace",
        "Standard DCF",
        "Biotech rNPV",
        "Saved Valuations",
        "Saved Reports",
        "Methodology",'''

if old_nav not in text:
    raise SystemExit("Could not find navigation list.")

text = text.replace(old_nav, new_nav, 1)

old_block = '''elif page == "Standard DCF":'''

new_block = '''elif page == "Research Workspace":

    page_header(
        "Research Workspace",
        "Company intelligence, research notes, valuation history, and reports."
    )

    selected_company = st.selectbox(
        "Select company",
        [
            "Neuralink",
            "Synchron",
            "Paradromics",
            "Blackrock Neurotech",
            "Precision Neuroscience",
        ],
    )

    section_title(
        selected_company,
        "Unified research profile"
    )

    profile_col, risk_col, action_col = st.columns([2, 1, 1])

    with profile_col:
        insight_card(
            "Company Profile",
            f"{selected_company} is tracked inside the Veles neurotechnology research universe. This workspace will consolidate company profile data, funding history, technology notes, valuation outputs, and generated reports."
        )

    with risk_col:
        activity_item(
            "Risk Profile",
            "Regulatory, clinical, technical, and commercialization risks will be summarized here.",
            "Research"
        )

    with action_col:
        activity_item(
            "Primary Action",
            "Generate valuation, create memo, or open saved model.",
            "Workspace"
        )

    section_title(
        "Research Modules",
        "The company workspace will eventually replace scattered pages."
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
        )

elif page == "Standard DCF":'''

if old_block not in text:
    raise SystemExit("Could not find Standard DCF block.")

text = text.replace(old_block, new_block, 1)

path.write_text(text)
print("UI patch 6 applied successfully: Research Workspace page added.")
