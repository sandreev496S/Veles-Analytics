from dotenv import load_dotenv

load_dotenv()

import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from styles import (
    load_veles_design_system,
    page_header,
    metric_card,
    insight_card,
    company_card,
    section_title,
    activity_item,
    status_pill,
    ai_workflow_card,
)
from services.auth import auth_ui, is_authenticated, get_current_user
from services.rate_limit import enforce_rate_limit
from services.errors import log_exception, safe_error_message
from services.report_storage import upload_report_bytes, create_signed_report_url, list_user_reports
from services.monitoring import capture_exception
from services.validation import (
    ValidationError,
    validate_standard_dcf_inputs,
    validate_biotech_inputs,
    validate_simulation_count,
)

from services.standard_dcf import run_dcf_case, sensitivity_matrix, calculate_wacc, reverse_dcf_growth, comparable_valuation
from services.pdf_report import create_dcf_pdf, create_rnpv_pdf
from services.ai_memo import generate_investment_memo, generate_biotech_memo
from services.excel_export import create_standard_dcf_excel, create_biotech_rnpv_excel
from components.dcf_wizard import render_dcf_wizard
from components.ui.navigation import render_sidebar_navigation
from components.ui.dashboard import render_research_terminal_header, render_analyst_command_center
from services.storage import save_valuation, list_valuations, load_valuation, delete_valuation
from services.supabase_storage import (
    save_valuation_supabase,
    list_valuations_supabase,
    load_valuation_supabase,
    delete_valuation_supabase,
)
from services.runtime_config import DEMO_MODE
from services.biotech_rnpv import run_biotech_rnpv, rnpv_sensitivity_matrix, run_monte_carlo_rnpv, biotech_tornado_analysis
from services.company_repository import (
    get_company_profiles,
    get_company_names,
    list_companies,
    create_company,
    update_company,
    delete_company,
)
from services.research_notes import (
    load_research_note,
    save_research_note,
    list_research_notes,
    delete_research_note,
)

from ui.crm_page import render_crm_page


# Keep the full interface usable without cloud credentials.  The UI was
# originally written against the Supabase-shaped functions below, so demo mode
# supplies small adapters over the existing local JSON storage rather than
# duplicating cloud/demo branches throughout every page.
if DEMO_MODE:
    def save_valuation_supabase(
        valuation_type,
        name,
        payload,
        user_id=None,
        company_name=None,
    ):
        return save_valuation(valuation_type, name, payload)


    def list_valuations_supabase(user_id=None):
        return [
            {
                **record,
                "id": record.get("file"),
                "company_name": record.get("company_name") or record.get("name"),
            }
            for record in list_valuations()
        ]


    def load_valuation_supabase(valuation_id, user_id=None):
        record = load_valuation(valuation_id)
        return {
            **record,
            "id": valuation_id,
            "company_name": record.get("company_name") or record.get("name"),
        }


    def delete_valuation_supabase(valuation_id, user_id=None):
        return delete_valuation(valuation_id)

st.set_page_config(
    page_title="Veles DCF Analyst",
    page_icon="⌁",
    layout="wide",
)
load_veles_design_system()

authenticated = auth_ui()

if not authenticated:
    st.stop()

st.session_state.setdefault("current_page", "Dashboard")
page = render_sidebar_navigation(st.session_state["current_page"])
st.session_state["current_page"] = page

page_header(
    "Veles Analytics",
    "Institutional AI research platform for neurotechnology and biotech."
)



if page == "Dashboard":

    try:
        valuations_count = len(
            list_valuations_supabase(
                user_id=get_current_user()["id"]
            )
        )
    except Exception:
        valuations_count = 0

    try:
        reports_count = len(
            list_user_reports(
                get_current_user()["id"]
            )
        )
    except Exception:
        reports_count = 0

    tracked_companies = get_company_profiles()

    render_research_terminal_header(
        coverage_count=len(tracked_companies.keys()),
        valuations_count=valuations_count,
        reports_count=reports_count,
        notes_count=0,
    )

    render_analyst_command_center()

    section_title(
        "Market Intelligence Terminal",
        "Funding signals, clinical milestones, regulatory events, and active coverage."
    )

    intelligence_col, coverage_col = st.columns([1.35, 1])

    with intelligence_col:
        st.markdown(
            '<div class="veles-mini-panel-title">Market Intelligence</div>',
            unsafe_allow_html=True,
        )

        activity_item(
            "Latest Funding Event",
            "Synchron remains a priority minimally invasive BCI company to monitor for future financing, clinical progress, and strategic investor activity.",
            "Funding Signal"
        )

        activity_item(
            "Latest Clinical Milestone",
            "Neuralink and other implantable BCI platforms should be tracked around human trial updates, safety outcomes, and device performance disclosures.",
            "Clinical Signal"
        )

        activity_item(
            "Latest Regulatory Event",
            "FDA progress, investigational device approvals, reimbursement positioning, and clinical trial expansion remain key valuation catalysts across the BCI universe.",
            "Regulatory Signal"
        )

        activity_item(
            "Priority Research Theme",
            "The strongest neurotechnology companies will combine clinical feasibility, durable data infrastructure, defensible hardware, and credible commercialization pathways.",
            "Research Lens"
        )

    with coverage_col:
        st.markdown(
            '<div class="veles-mini-panel-title">Coverage Universe</div>',
            unsafe_allow_html=True,
        )

        if tracked_companies:
            for company_name, company_data in list(tracked_companies.items())[:6]:
                activity_item(
                    company_name,
                    f'{company_data["stage"]} · {company_data["valuation"]}',
                    company_data["funding"],
                )
        else:
            activity_item(
                "No Companies Found",
                "Seed the companies table in Supabase to populate the Dashboard coverage universe.",
                "Company Database"
            )

    section_title("Operational Activity", "Timeline of recent valuation, research, and reporting actions.")

    timeline_col1, timeline_col2, timeline_col3 = st.columns(3)

    with timeline_col1:
        st.markdown(
            '<div class="veles-mini-panel-title">Today</div>',
            unsafe_allow_html=True,
        )

        activity_item(
            "Generated Neuralink DCF",
            "Base case intrinsic valuation model created with scenario comparison and sensitivity matrix.",
            "Valuation"
        )

        activity_item(
            "Updated Neurotech Watchlist",
            "Core BCI competitor universe refreshed for company research tracking.",
            "Workspace"
        )

    with timeline_col2:
        st.markdown(
            '<div class="veles-mini-panel-title">Yesterday</div>',
            unsafe_allow_html=True,
        )

        activity_item(
            "Saved Biotech rNPV Model",
            "Risk-adjusted valuation model saved for future analysis and report generation.",
            "Saved Models"
        )

    with timeline_col3:
        st.markdown(
            '<div class="veles-mini-panel-title">This Week</div>',
            unsafe_allow_html=True,
        )

        activity_item(
            "Prepared Monte Carlo Output",
            "Simulation distribution and percentile table ready for analyst review.",
            "Analysis"
        )

        activity_item(
            "Report Export Ready",
            "PDF and Excel report outputs are available for saved valuation models.",
            "Reports"
        )

elif page == "Clients":
    render_crm_page()


elif page == "Companies":

    page_header(
        "Companies",
        "Manage the company intelligence database used across Veles."
    )

    companies = list_companies()
    st.session_state.setdefault("companies_action", "add")

    st.markdown(
        f"""
        <div class="veles-company-terminal-hero">
            <div class="veles-company-terminal-kicker">Company Intelligence Database</div>
            <div class="veles-company-terminal-title">Coverage Universe</div>
            <div class="veles-company-terminal-subtitle">
                Tracked companies, technology modalities, funding profiles, and research workspace coverage.
            </div>
            <div class="veles-company-terminal-description">
                Maintain the core Veles company universe used across research workspaces, valuation models, reports, and AI-generated investment memos.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not companies:
        activity_item(
            "No Companies Found",
            "Add your first company below to populate the research workspace.",
            "Company Database"
        )

    section_title(
        "Company Actions",
        "Choose an action to manage the company intelligence database."
    )

    action_col1, action_col2, action_col3 = st.columns(3)

    with action_col1:
        if st.button("＋ Add Company", key="companies_action_add", use_container_width=True):
            st.session_state["companies_action"] = "add"
            st.rerun()

    with action_col2:
        if st.button("✎ Edit Company", key="companies_action_edit", use_container_width=True):
            st.session_state["companies_action"] = "edit"
            st.rerun()

    with action_col3:
        if st.button("⌫ Delete Company", key="companies_action_delete", use_container_width=True):
            st.session_state["companies_action"] = "delete"
            st.rerun()

    section_title(
        "Workspace Launcher",
        "Open a company in the Research Workspace."
    )

    if companies:
        workspace_company = st.selectbox(
            "Choose company to research",
            [company["name"] for company in companies],
            key="companies_workspace_select",
        )

        activity_item(
            f"Open {workspace_company}",
            "Go to Research Workspace from the sidebar and select this company to view reports, models, notes, funding, technology, and competition.",
            "Research Workspace"
        )
    else:
        activity_item(
            "No Workspace Available",
            "Add a company first to enable research workspace navigation.",
            "Research Workspace"
        )

    if st.session_state.get("companies_action") == "add":
        section_title(
            "Add Company",
            "Create a new company profile for the research workspace."
        )

        with st.form("add_company_form"):
            col1, col2 = st.columns(2)

            with col1:
                new_name = st.text_input("Company name")
                new_sector = st.text_input("Sector", value="Neurotechnology")
                new_focus = st.text_input("Focus")

            with col2:
                new_modality = st.text_input("Modality")
                new_stage = st.text_input("Stage")
                new_funding = st.text_input("Funding")
                new_valuation = st.text_input("Valuation")
                new_website = st.text_input("Website")

            new_risk = st.text_area("Risk profile")

            submitted = st.form_submit_button("Add Company")

            if submitted:
                if not new_name:
                    st.error("Company name is required.")
                else:
                    create_company(
                        name=new_name,
                        sector=new_sector,
                        focus=new_focus,
                        modality=new_modality,
                        stage=new_stage,
                        funding=new_funding,
                        valuation=new_valuation,
                        risk=new_risk,
                        website=new_website,
                    )
                    st.success(f"Added company: {new_name}")
                    st.rerun()

    if st.session_state.get("companies_action") == "edit":
        section_title(
            "Edit Company",
            "Update an existing company profile."
        )

        companies = list_companies()

        if companies:
            company_options = {
                company["name"]: company
                for company in companies
            }

            selected_edit_company = st.selectbox(
                "Select company to edit",
                list(company_options.keys()),
                key="edit_company_select",
            )

            selected_company_record = company_options[selected_edit_company]

            with st.form("edit_company_form"):
                col1, col2 = st.columns(2)

                with col1:
                    edit_name = st.text_input("Company name", value=selected_company_record.get("name") or "")
                    edit_sector = st.text_input("Sector", value=selected_company_record.get("sector") or "")
                    edit_focus = st.text_input("Focus", value=selected_company_record.get("focus") or "")

                with col2:
                    edit_modality = st.text_input("Modality", value=selected_company_record.get("modality") or "")
                    edit_stage = st.text_input("Stage", value=selected_company_record.get("stage") or "")
                    edit_funding = st.text_input("Funding", value=selected_company_record.get("funding") or "")
                    edit_valuation = st.text_input("Valuation", value=selected_company_record.get("valuation") or "")
                    edit_website = st.text_input("Website", value=selected_company_record.get("website") or "")

                edit_risk = st.text_area("Risk profile", value=selected_company_record.get("risk") or "")

                edit_submitted = st.form_submit_button("Update Company")

                if edit_submitted:
                    update_company(
                        selected_company_record["id"],
                        name=edit_name,
                        sector=edit_sector,
                        focus=edit_focus,
                        modality=edit_modality,
                        stage=edit_stage,
                        funding=edit_funding,
                        valuation=edit_valuation,
                        risk=edit_risk,
                        website=edit_website,
                    )
                    st.success(f"Updated company: {edit_name}")
                    st.rerun()
        else:
            activity_item(
                "No Companies Available",
                "Add a company before using the edit workflow.",
                "Company Database"
            )

    if st.session_state.get("companies_action") == "delete":
        section_title(
            "Delete Company",
            "Remove a company from the intelligence database."
        )

        companies = list_companies()

        if companies:
            delete_options = {
                company["name"]: company
                for company in companies
            }

            selected_delete_company = st.selectbox(
                "Select company to delete",
                list(delete_options.keys()),
                key="delete_company_select",
            )

            selected_delete_record = delete_options[selected_delete_company]

            st.warning(
                "Deleting a company removes it from the company database. Existing reports, notes, and valuations may still remain separately stored."
            )

            confirm_delete = st.checkbox(
                f"I understand and want to delete {selected_delete_company}",
                key="confirm_delete_company",
            )

            if st.button("Delete Company", key="delete_company_button"):
                if not confirm_delete:
                    st.error("Confirm deletion before continuing.")
                else:
                    delete_company(selected_delete_record["id"])
                    st.success(f"Deleted company: {selected_delete_company}")
                    st.rerun()
        else:
            activity_item(
                "No Companies Available",
                "There are no companies available to delete.",
                "Company Database"
            )


elif page == "Research Workspace":

    page_header(
        "Research Workspace",
        "Company intelligence, research notes, valuation history, and reports."
    )

    company_profiles = get_company_profiles()

    if not company_profiles:
        activity_item(
            "No Companies Found",
            "Seed the companies table in Supabase before using the Research Workspace.",
            "Company Database"
        )
        st.stop()

    selected_company = st.selectbox(
        "Select company",
        list(company_profiles.keys()),
    )

    if not selected_company:
        activity_item(
            "No Company Selected",
            "Select a company to open its research workspace.",
            "Company Database"
        )
        st.stop()

    selected_profile = company_profiles[selected_company]

    st.markdown(
        f"""
        <div class="veles-company-terminal-hero">
            <div class="veles-company-terminal-kicker">Company Terminal</div>
            <div class="veles-company-terminal-title">{selected_company}</div>
            <div class="veles-company-terminal-subtitle">
                {selected_profile["stage"]} · {selected_profile["modality"]} · {selected_profile["valuation"]}
            </div>
            <div class="veles-company-terminal-description">
                Unified intelligence workspace for company profile, technology, funding, competition, valuations, notes, and reports.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        metric_card("Technology", selected_profile["modality"], "Modality")

    with k2:
        metric_card("Stage", selected_profile["stage"], "Company Status")

    with k3:
        metric_card("Funding", selected_profile["funding"], "Known Capital")

    with k4:
        metric_card("Valuation", selected_profile["valuation"], "Latest Known")

    with k5:
        metric_card("Risk", selected_profile["risk"], "Research Flag")

    section_title(
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

    section_title(
        "Company Intelligence Terminal",
        "Structured research, technology, funding, competition, valuation, notes, and report workspace."
    )

    overview_tab, tech_tab, funding_tab, competition_tab, valuation_tab, notes_tab, reports_tab = st.tabs(
        [
            "Overview",
            "Technology",
            "Funding",
            "Competition",
            "Valuations",
            "Research Notes",
            "Reports",
        ]
    )

    with overview_tab:
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

    with funding_tab:
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

    with tech_tab:
        section_title(
            "Technology Profile",
            "Modality, focus area, technical positioning, advantages, and research risks."
        )

        tech_k1, tech_k2, tech_k3 = st.columns(3)

        with tech_k1:
            metric_card("Modality", selected_profile["modality"], "Technology Type")

        with tech_k2:
            metric_card("Focus", selected_profile["focus"], "Use Case")

        with tech_k3:
            metric_card("Status", selected_profile["stage"], "Clinical / Company Stage")

        tech_left, tech_right = st.columns([1.35, 1])

        with tech_left:
            insight_card(
                "Technology Intelligence",
                f"{selected_company}'s technical diligence should focus on modality, invasiveness, signal quality, surgical burden, device durability, software stack, neural data infrastructure, and scalability of deployment."
            )

            technology_profile = pd.DataFrame([
                {
                    "Company": selected_company,
                    "Focus": selected_profile["focus"],
                    "Modality": selected_profile["modality"],
                    "Technical Status": "Tracked",
                    "Clinical / Company Stage": selected_profile["stage"],
                    "Primary Risk": selected_profile["risk"],
                }
            ])

            st.dataframe(technology_profile, use_container_width=True)

        with tech_right:
            activity_item(
                "Potential Advantages",
                "Assess differentiation in signal acquisition, hardware design, implantation burden, usability, software integration, and defensibility of neural datasets.",
                "Advantage"
            )

            activity_item(
                "Technical Risks",
                selected_profile["risk"],
                "Risk"
            )

            activity_item(
                "Next Data Sources",
                "Connect patents, papers, device specifications, clinical trial updates, FDA filings, and technical publications.",
                "Data Pipeline"
            )

    with competition_tab:
        section_title(
            "Competitive Landscape",
            "Peer universe, differentiation analysis, and strategic positioning."
        )

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

        peer_col1, peer_col2, peer_col3 = st.columns(3)

        with peer_col1:
            metric_card("Coverage Universe", len(competition_df), "Tracked Peers")

        with peer_col2:
            invasive_count = (competition_df["Modality"] == "Invasive").sum()
            metric_card("Invasive Platforms", invasive_count, "Peer Mix")

        with peer_col3:
            minimally_invasive_count = competition_df["Modality"].str.contains("Minimally", case=False, na=False).sum()
            metric_card("Minimally Invasive", minimally_invasive_count, "Platforms")

        st.dataframe(competition_df, use_container_width=True)

        section_title(
            "Competitive Positioning",
            "Technical, clinical, commercial, and capitalization differentiation."
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

        section_title(
            "Competitive Scorecard",
            "Relative positioning across technology, clinical maturity, capitalization, and regulatory risk."
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

        st.dataframe(scoring_df, use_container_width=True)

        activity_item(
            "Strategic Takeaway",
            "This scorecard is a first-pass qualitative model. Next step: replace static scores with analyst inputs, saved diligence notes, and stored company-level research data.",
            "Competitive Intelligence"
        )

    with valuation_tab:
        section_title(
            "Valuation Intelligence",
            "Saved models, linked valuation outputs, and export readiness."
        )

        try:
            valuation_records = list_valuations_supabase(
                user_id=get_current_user()["id"]
            )

            company_records = [
                record for record in valuation_records
                if (
                    str(record.get("company_name", "")).lower() == selected_company.lower()
                    or selected_company.lower() in str(record.get("name", "")).lower()
                )
            ]

            val_k1, val_k2, val_k3 = st.columns(3)

            with val_k1:
                metric_card("Linked Models", len(company_records), selected_company)

            with val_k2:
                metric_card("Model Types", "DCF / rNPV", "Supported")

            with val_k3:
                metric_card("Export Status", "Ready", "PDF / Excel")

            valuation_left, valuation_right = st.columns([1.4, 1])

            with valuation_left:
                if company_records:
                    valuation_df = pd.DataFrame(company_records)
                    st.dataframe(valuation_df, use_container_width=True)
                else:
                    activity_item(
                        "No Saved Models Yet",
                        f"No saved valuation models are currently linked to {selected_company}. Run a DCF or rNPV model and save it to populate this tab.",
                        "Models"
                    )

            with valuation_right:
                activity_item(
                    "Latest Valuation",
                    "Use saved DCF or rNPV outputs to build company-level valuation history and investment memo context.",
                    "Valuation"
                )

                activity_item(
                    "Scenario Analysis",
                    "Next step: surface downside, base case, upside, sensitivity, and implied growth outputs directly inside this company terminal.",
                    "Model Intelligence"
                )

                activity_item(
                    "Export Center",
                    "Reports and model exports should be accessible from this tab once linked to the company profile.",
                    "Reports"
                )

        except Exception as e:
            log_exception("research_workspace_valuation_history", e)
            activity_item(
                "Valuation History Unavailable",
                "Could not load saved valuation models right now.",
                "Error"
            )

    with notes_tab:
        user_id = get_current_user()["id"]

        section_title(
            "Analyst Notebook",
            f"Persistent research notes, thesis development, catalysts, risks, and diligence questions for {selected_company}."
        )

        general_note_record = load_research_note(
            user_id=user_id,
            company_name=selected_company,
            note_type="general",
        )

        thesis_record = load_research_note(
            user_id=user_id,
            company_name=selected_company,
            note_type="thesis",
        )

        catalysts_record = load_research_note(
            user_id=user_id,
            company_name=selected_company,
            note_type="catalysts",
        )

        risks_record = load_research_note(
            user_id=user_id,
            company_name=selected_company,
            note_type="risks",
        )

        questions_record = load_research_note(
            user_id=user_id,
            company_name=selected_company,
            note_type="questions",
        )

        notes_left, notes_right = st.columns([1.25, 1])

        with notes_left:
            st.markdown(
                '<div class="veles-mini-panel-title">Company Research Note</div>',
                unsafe_allow_html=True,
            )

            note_text = st.text_area(
                "Company research note",
                value=(general_note_record or {}).get("content", ""),
                height=320,
                placeholder="Write thesis updates, risks, catalysts, diligence questions, funding notes, or technical observations here.",
                key=f"research_note_input_{selected_company}",
            )

            if st.button(
                "Save Research Note",
                key=f"save_research_note_{selected_company}",
            ):
                save_research_note(
                    user_id=user_id,
                    company_name=selected_company,
                    note_type="general",
                    content=note_text,
                )
                st.success(f"Research note saved for {selected_company}.")
                st.rerun()

        with notes_right:
            st.markdown(
                '<div class="veles-mini-panel-title">Research Structure</div>',
                unsafe_allow_html=True,
            )

            activity_item(
                "Notebook Scope",
                "Capture thesis updates, catalysts, risks, technical observations, funding notes, diligence questions, and report ideas.",
                "Analyst Notes"
            )

            activity_item(
                "Research Workflow",
                "Use structured fields below to separate investment thesis, catalysts, risks, and open questions.",
                "Workflow"
            )

        section_title(
            "Structured Thesis Workspace",
            "Institutional diligence fields for thesis, catalysts, risks, and open questions."
        )

        thesis_col, catalysts_col = st.columns(2)

        with thesis_col:
            thesis = st.text_area(
                "Thesis",
                value=(thesis_record or {}).get("content", ""),
                height=160,
                key=f"thesis_input_{selected_company}",
            )

        with catalysts_col:
            catalysts = st.text_area(
                "Catalysts",
                value=(catalysts_record or {}).get("content", ""),
                height=160,
                key=f"catalysts_input_{selected_company}",
            )

        risks_col, questions_col = st.columns(2)

        with risks_col:
            risks = st.text_area(
                "Risks",
                value=(risks_record or {}).get("content", ""),
                height=160,
                key=f"risks_input_{selected_company}",
            )

        with questions_col:
            questions = st.text_area(
                "Open Questions",
                value=(questions_record or {}).get("content", ""),
                height=160,
                key=f"questions_input_{selected_company}",
            )

        if st.button(
            "Draft Thesis From Company Profile",
            key=f"draft_thesis_{selected_company}",
        ):
            draft_thesis = (
                f"{selected_company} is positioned within the {selected_profile['focus']} segment of neurotechnology. "
                f"The company may be attractive if it can convert technical differentiation into clinical adoption, regulatory progress, and durable market leadership."
            )

            save_research_note(user_id, selected_company, "thesis", draft_thesis)
            save_research_note(
                user_id,
                selected_company,
                "catalysts",
                "Clinical progress; regulatory milestones; new funding rounds; strategic partnerships; published performance data.",
            )
            save_research_note(user_id, selected_company, "risks", selected_profile["risk"])
            save_research_note(
                user_id,
                selected_company,
                "questions",
                "What is the clearest regulatory pathway? What evidence supports commercial adoption? How differentiated is the technology versus direct competitors? What valuation is justified by current traction?",
            )

            st.success(f"Draft thesis created for {selected_company}.")
            st.rerun()

        if st.button(
            "Save Thesis Workspace",
            key=f"save_thesis_workspace_{selected_company}",
        ):
            save_research_note(user_id, selected_company, "thesis", thesis)
            save_research_note(user_id, selected_company, "catalysts", catalysts)
            save_research_note(user_id, selected_company, "risks", risks)
            save_research_note(user_id, selected_company, "questions", questions)

            st.success(f"Investment thesis workspace saved for {selected_company}.")
            st.rerun()

        company_notes = list_research_notes(
            user_id=user_id,
            company_name=selected_company,
        )

        section_title(
            "Saved Research Log",
            "Stored note records linked to this company."
        )

        if company_notes:
            notes_df = pd.DataFrame(company_notes)
            st.dataframe(notes_df, use_container_width=True)
        else:
            activity_item(
                "No Saved Notes Yet",
                "Use the fields above to start building a persistent company-specific research log.",
                "Notes"
            )

    with reports_tab:
        section_title(
            "Report Library",
            "Cloud-stored reports, model exports, and signed report access."
        )

        try:
            report_records = list_user_reports(
                get_current_user()["id"]
            )

            company_reports = [
                report for report in report_records
                if (
                    str(report.get("company_name", "")).lower() == selected_company.lower()
                    or selected_company.lower() in str(report.get("file_name", "")).lower()
                )
            ]

            report_k1, report_k2, report_k3 = st.columns(3)

            with report_k1:
                metric_card("Linked Reports", len(company_reports), selected_company)

            with report_k2:
                metric_card("Formats", "PDF / Excel", "Supported")

            with report_k3:
                metric_card("Access", "Signed URLs", "Secure Links")

            reports_left, reports_right = st.columns([1.4, 1])

            with reports_left:
                if company_reports:
                    reports_df = pd.DataFrame(company_reports)
                    st.dataframe(reports_df, use_container_width=True)
                else:
                    activity_item(
                        "No Saved Reports Yet",
                        f"No cloud reports are currently linked to {selected_company}. Generate and save a PDF or Excel model to populate this tab.",
                        "Reports"
                    )

            with reports_right:
                activity_item(
                    "Latest Memo",
                    "AI investment memos and valuation reports linked to this company will appear in the report library.",
                    "Memo"
                )

                activity_item(
                    "Export Center",
                    "PDF reports, Excel models, and future board-style memos should be accessible from this company terminal.",
                    "Exports"
                )

                activity_item(
                    "Secure Access",
                    "Signed report links provide controlled temporary access to files stored in cloud storage.",
                    "Storage"
                )

                if company_reports:
                    report_options = {
                        f"{report.get('file_name')} | {report.get('report_type')} | {report.get('created_at')}": report.get("storage_path")
                        for report in company_reports
                    }

                    selected_report = st.selectbox(
                        "Open company report",
                        list(report_options.keys()),
                        key=f"research_workspace_report_select_{selected_company}",
                    )

                    if st.button(
                        "Create Signed Report Link",
                        key=f"research_workspace_signed_link_{selected_company}",
                    ):
                        signed_url = create_signed_report_url(
                            report_options[selected_report]
                        )

                        if signed_url:
                            st.success("Signed report link created.")
                            st.write(signed_url)
                            st.link_button("Open Report", signed_url)
                        else:
                            st.error("Could not create signed report link.")

        except Exception as e:
            log_exception("research_workspace_reports", e)
            activity_item(
                "Reports Unavailable",
                "Could not load saved reports right now.",
                "Error"
            )

elif page == "Standard DCF":
    render_dcf_wizard(
        page_header=page_header,
        section_title=section_title,
        metric_card=metric_card,
        activity_item=activity_item,
    )

elif page == "Biotech rNPV":
    page_header(
        "Biotech rNPV Builder",
        "Institutional probability-adjusted valuation workflow for biotech, medtech, and neurotechnology assets."
    )

    section_title(
        "Asset & Market Assumptions",
        "Define the asset profile, market opportunity, clinical stage, launch timing, and probability of approval."
    )

    section_title(
        "Workspace Settings",
        "Manage account, storage, billing, security, data sources, and workspace preferences."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        asset_name = st.text_input("Asset / company name", value="Neuralink")
        eligible_patients = st.number_input("Eligible patient population", value=1000000)
        price_per_treatment = st.number_input("Price per treatment/device ($)", value=50000)

    with col2:
        launch_year = st.slider("Launch year in forecast", 1, 10, 5)
        forecast_years = st.slider("Forecast years", 5, 20, 12)
        years_to_peak = st.slider("Years to peak penetration", 1, 10, 6)

    with col3:
        clinical_stage = st.selectbox(
            "Clinical / regulatory stage",
            [
                "Preclinical",
                "Phase I",
                "Phase II",
                "Phase III",
                "Approved",
                "Custom",
            ],
            index=2,
        )

        stage_probabilities = {
            "Preclinical": 0.05,
            "Phase I": 0.10,
            "Phase II": 0.20,
            "Phase III": 0.55,
            "Approved": 0.95,
            "Custom": 0.20,
        }

        peak_penetration = st.number_input("Peak market penetration", value=0.05, format="%.3f")

        probability_of_approval = st.number_input(
            "Probability of approval",
            value=stage_probabilities[clinical_stage],
            format="%.3f",
        )

        operating_margin = st.number_input("Operating margin", value=0.35, format="%.3f")

    section_title(
        "Financial & Risk Assumptions",
        "Define discount rate, tax rate, R&D cost, launch cost, cash, debt, shares, and current market value."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        tax_rate = st.number_input("Tax rate", value=0.21, format="%.3f")
        discount_rate = st.number_input("Discount rate", value=0.18, format="%.3f")

    with col2:
        annual_rd_cost = st.number_input("Annual R&D cost before launch ($M)", value=150.0)
        launch_cost = st.number_input("Launch/commercialization cost ($M)", value=500.0)

    with col3:
        cash = st.number_input("Cash ($M)", value=1000.0)
        debt = st.number_input("Debt ($M)", value=0.0)
        shares = st.number_input("Fully diluted shares (M)", value=100.0)
        current_market_cap = st.number_input("Current market cap ($M)", value=5000.0)

    run_rnpv = st.toggle("Auto-run rNPV model", value=True)

    if run_rnpv:
        try:
            validated_biotech_inputs = validate_biotech_inputs(
                asset_name=asset_name,
                eligible_patients=eligible_patients,
                price_per_treatment=price_per_treatment,
                launch_year=launch_year,
                forecast_years=forecast_years,
                years_to_peak=years_to_peak,
                peak_penetration=peak_penetration,
                probability_of_approval=probability_of_approval,
                operating_margin=operating_margin,
                tax_rate=tax_rate,
                discount_rate=discount_rate,
                annual_rd_cost=annual_rd_cost,
                launch_cost=launch_cost,
                cash=cash,
                debt=debt,
                shares=shares,
                current_market_cap=current_market_cap,
            )
        except ValidationError as e:
            st.error(str(e))
            st.stop()

        asset_name = validated_biotech_inputs["asset_name"]
        eligible_patients = validated_biotech_inputs["eligible_patients"]
        price_per_treatment = validated_biotech_inputs["price_per_treatment"]
        launch_year = validated_biotech_inputs["launch_year"]
        forecast_years = validated_biotech_inputs["forecast_years"]
        years_to_peak = validated_biotech_inputs["years_to_peak"]
        peak_penetration = validated_biotech_inputs["peak_penetration"]
        probability_of_approval = validated_biotech_inputs["probability_of_approval"]
        operating_margin = validated_biotech_inputs["operating_margin"]
        tax_rate = validated_biotech_inputs["tax_rate"]
        discount_rate = validated_biotech_inputs["discount_rate"]
        annual_rd_cost = validated_biotech_inputs["annual_rd_cost"]
        launch_cost = validated_biotech_inputs["launch_cost"]
        cash = validated_biotech_inputs["cash"]
        debt = validated_biotech_inputs["debt"]
        shares = validated_biotech_inputs["shares"]
        current_market_cap = validated_biotech_inputs["current_market_cap"]

        rnpv_df, rnpv_valuation = run_biotech_rnpv(
            asset_name=asset_name,
            launch_year=launch_year,
            forecast_years=forecast_years,
            eligible_patients=eligible_patients,
            price_per_treatment=price_per_treatment,
            peak_penetration=peak_penetration,
            years_to_peak=years_to_peak,
            probability_of_approval=probability_of_approval,
            operating_margin=operating_margin,
            tax_rate=tax_rate,
            discount_rate=discount_rate,
            annual_rd_cost=annual_rd_cost,
            launch_cost=launch_cost,
            cash=cash,
            debt=debt,
            shares=shares,
        )

        section_title("rNPV Valuation Summary", "Probability-adjusted enterprise value, equity value, implied share price, and approval risk.")

        st.info(f"Clinical / regulatory stage: {clinical_stage} | Probability of approval: {probability_of_approval:.1%}")

        rnpv_valuation_df = pd.DataFrame(
            rnpv_valuation.items(),
            columns=["Metric", "Value"],
        )

        rnpv_lookup = dict(rnpv_valuation)
        rnpv_kpi1, rnpv_kpi2, rnpv_kpi3, rnpv_kpi4 = st.columns(4)

        with rnpv_kpi1:
            metric_card(
                "Asset rNPV / EV",
                f"${rnpv_lookup.get('Asset rNPV / Enterprise Value ($M)', 0):,.1f}M",
                "Risk-Adjusted"
            )

        with rnpv_kpi2:
            metric_card(
                "Equity Value",
                f"${rnpv_lookup.get('Equity Value ($M)', 0):,.1f}M",
                "After Cash / Debt"
            )

        with rnpv_kpi3:
            metric_card(
                "Implied Share Price",
                f"${rnpv_lookup.get('Implied Share Price ($)', 0):,.2f}",
                "Per Share"
            )

        with rnpv_kpi4:
            metric_card(
                "Approval Probability",
                f"{rnpv_lookup.get('Probability of Approval', probability_of_approval):.1%}",
                clinical_stage
            )

        section_title(
            f"{asset_name} Investment Snapshot",
            clinical_stage
        )

        snapshot_col1, snapshot_col2, snapshot_col3, snapshot_col4 = st.columns(4)

        with snapshot_col1:
            metric_card(
                "Eligible Patients",
                f"{eligible_patients:,.0f}",
                "Market Size"
            )

        with snapshot_col2:
            metric_card(
                "Price / Treatment",
                f"${price_per_treatment:,.0f}",
                "Economics"
            )

        with snapshot_col3:
            metric_card(
                "Peak Penetration",
                f"{peak_penetration:.1%}",
                "Commercialization"
            )

        with snapshot_col4:
            metric_card(
                "Approval Probability",
                f"{probability_of_approval:.1%}",
                clinical_stage
            )

        section_title("Forecast Overview", "Compact visual summary of revenue and risk-adjusted value trajectory.")

        if rnpv_df is not None and not rnpv_df.empty:
            chart_col1, chart_col2 = st.columns(2)

            if "Year" in rnpv_df.columns and "Revenue ($M)" in rnpv_df.columns:
                rnpv_revenue_chart = px.line(
                    rnpv_df,
                    x="Year",
                    y="Revenue ($M)",
                    markers=True,
                    title="Revenue Forecast",
                )
                rnpv_revenue_chart.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20),
                )

                with chart_col1:
                    st.plotly_chart(
                        rnpv_revenue_chart,
                        use_container_width=True,
                        key="rnpv_revenue_chart_compact",
                    )

            value_columns = [
                col for col in rnpv_df.columns
                if "Value" in col or "rNPV" in col or "PV" in col
            ]

            if "Year" in rnpv_df.columns and value_columns:
                rnpv_value_chart = px.line(
                    rnpv_df,
                    x="Year",
                    y=value_columns[0],
                    markers=True,
                    title="Risk-Adjusted Value",
                )
                rnpv_value_chart.update_layout(
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20),
                )

                with chart_col2:
                    st.plotly_chart(
                        rnpv_value_chart,
                        use_container_width=True,
                        key="rnpv_value_chart_compact",
                    )

        with st.expander("View Probability-Adjusted Forecast Table", expanded=False):
            st.dataframe(rnpv_df, use_container_width=True)

        section_title("Sensitivity Analysis", "Implied share price sensitivity across probability and discount-rate assumptions.")

        rnpv_sens_df = rnpv_sensitivity_matrix(
            asset_name=asset_name,
            launch_year=launch_year,
            forecast_years=forecast_years,
            eligible_patients=eligible_patients,
            price_per_treatment=price_per_treatment,
            peak_penetration=peak_penetration,
            years_to_peak=years_to_peak,
            operating_margin=operating_margin,
            tax_rate=tax_rate,
            annual_rd_cost=annual_rd_cost,
            launch_cost=launch_cost,
            cash=cash,
            debt=debt,
            shares=shares,
        )

        with st.expander("View Sensitivity Matrix", expanded=False):
            st.dataframe(rnpv_sens_df, use_container_width=True)

        with st.expander("Risk Analysis Suite", expanded=False):
            section_title("Risk Analysis", "Monte Carlo simulation, valuation distribution, percentile outcomes, and scenario risk.")

            simulations = st.slider(
                "Number of simulations",
                min_value=1000,
                max_value=10000,
                value=10000,
                step=1000,
            )

            try:
                simulations = validate_simulation_count(simulations, max_allowed=10000)
            except ValidationError as e:
                st.error(str(e))
                st.stop()

            enforce_rate_limit("monte_carlo_rnpv", limit=30, window_seconds=3600, user_id=get_current_user()["id"])

            mc_results_df, mc_summary = run_monte_carlo_rnpv(
                asset_name=asset_name,
                launch_year=launch_year,
                forecast_years=forecast_years,
                eligible_patients=eligible_patients,
                base_price_per_treatment=price_per_treatment,
                base_peak_penetration=peak_penetration,
                years_to_peak=years_to_peak,
                base_probability_of_approval=probability_of_approval,
                base_operating_margin=operating_margin,
                tax_rate=tax_rate,
                base_discount_rate=discount_rate,
                annual_rd_cost=annual_rd_cost,
                launch_cost=launch_cost,
                cash=cash,
                debt=debt,
                shares=shares,
                current_market_cap=current_market_cap,
                simulations=simulations,
            )

            mc_summary_df = pd.DataFrame(
                mc_summary.items(),
                columns=["Metric", "Value"],
            )

            st.dataframe(mc_summary_df, use_container_width=True)

            monte_carlo_hist = px.histogram(
                mc_results_df,
                x="Enterprise Value ($M)",
                nbins=60,
                title=f"{asset_name} Monte Carlo rNPV Distribution",
            )
            st.plotly_chart(monte_carlo_hist, use_container_width=True)

            percentile_df = pd.DataFrame({
                "Percentile": ["5th", "25th", "50th", "75th", "95th"],
                "Enterprise Value ($M)": [
                    mc_results_df["Enterprise Value ($M)"].quantile(0.05),
                    mc_results_df["Enterprise Value ($M)"].quantile(0.25),
                    mc_results_df["Enterprise Value ($M)"].quantile(0.50),
                    mc_results_df["Enterprise Value ($M)"].quantile(0.75),
                    mc_results_df["Enterprise Value ($M)"].quantile(0.95),
                ],
            })

            section_title("Monte Carlo Percentiles", "Distribution percentiles for simulated enterprise value outcomes.")
            st.dataframe(percentile_df, use_container_width=True)

            section_title("Key Valuation Drivers", "Variables with the greatest impact on enterprise value.")

            tornado_df = biotech_tornado_analysis(
                asset_name=asset_name,
                launch_year=launch_year,
                forecast_years=forecast_years,
                eligible_patients=eligible_patients,
                price_per_treatment=price_per_treatment,
                peak_penetration=peak_penetration,
                years_to_peak=years_to_peak,
                probability_of_approval=probability_of_approval,
                operating_margin=operating_margin,
                tax_rate=tax_rate,
                discount_rate=discount_rate,
                annual_rd_cost=annual_rd_cost,
                launch_cost=launch_cost,
                cash=cash,
                debt=debt,
                shares=shares,
            )

            st.dataframe(tornado_df, use_container_width=True)

            tornado_chart = px.bar(
                tornado_df,
                x="Impact Range ($M)",
                y="Variable",
                orientation="h",
                title=f"{asset_name} Tornado Analysis — EV Sensitivity",
            )

            tornado_chart.update_layout(
                yaxis={"categoryorder": "total ascending"}
            )

            st.plotly_chart(tornado_chart, use_container_width=True)

            section_title("Monte Carlo CDF", "Probability that simulated enterprise value falls below or exceeds a selected threshold.")

            sorted_ev = mc_results_df["Enterprise Value ($M)"].sort_values().reset_index(drop=True)
            cdf_df = pd.DataFrame({
                "Enterprise Value ($M)": sorted_ev,
                "Cumulative Probability": [(i + 1) / len(sorted_ev) for i in range(len(sorted_ev))],
            })

            cdf_chart = px.line(
                cdf_df,
                x="Enterprise Value ($M)",
                y="Cumulative Probability",
                title=f"{asset_name} Monte Carlo CDF",
            )

            st.plotly_chart(cdf_chart, use_container_width=True)

            threshold = st.number_input(
                "Valuation threshold ($M)",
                value=float(current_market_cap),
            )

            probability_above_threshold = (
                mc_results_df["Enterprise Value ($M)"] > threshold
            ).mean()

            st.metric(
                "Probability EV Exceeds Threshold",
                f"{probability_above_threshold:.1%}",
            )

        rnpv_valuation_df = pd.DataFrame(
            rnpv_valuation.items(),
            columns=["Metric", "Value"],
        )

        st.session_state["rnpv_outputs"] = {
            "asset_name": asset_name,
            "clinical_stage": clinical_stage,
            "valuation_df": rnpv_valuation_df,
            "forecast_df": rnpv_df,
            "sensitivity_df": rnpv_sens_df,
            "monte_carlo_summary_df": mc_summary_df if "mc_summary_df" in locals() else pd.DataFrame(),
            "monte_carlo_percentile_df": percentile_df if "percentile_df" in locals() else pd.DataFrame(),
            "tornado_df": tornado_df if "tornado_df" in locals() else pd.DataFrame(),
        }

        section_title(
            "Actions Center",
            "Exports, cloud storage, AI memo generation, and valuation management."
        )

        rnpv_pdf = create_rnpv_pdf(
            asset_name=asset_name,
            valuation_df=rnpv_valuation_df,
            forecast_df=rnpv_df,
            clinical_stage=clinical_stage,
        )

        biotech_excel = create_biotech_rnpv_excel(
            asset_name=asset_name,
            valuation_df=rnpv_valuation_df,
            forecast_df=rnpv_df,
            clinical_stage=clinical_stage,
            sensitivity_df=rnpv_sens_df,
            monte_carlo_summary_df=mc_summary_df if "mc_summary_df" in locals() else None,
            monte_carlo_percentile_df=percentile_df if "percentile_df" in locals() else None,
            tornado_df=tornado_df if "tornado_df" in locals() else None,
        )

        pdf_col, excel_col = st.columns(2)

        with pdf_col:
            st.markdown('<div class="veles-mini-panel-title">PDF Report</div>', unsafe_allow_html=True)

            st.download_button(
                label="Download Biotech rNPV Report",
                data=rnpv_pdf,
                file_name=f"{asset_name.lower().replace(' ', '_')}_rnpv_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

            if st.button("Save PDF to Cloud", key="save_biotech_pdf_cloud", use_container_width=True):
                try:
                    report_id, storage_path = upload_report_bytes(
                        user_id=get_current_user()["id"],
                        report_type="biotech_rnpv_pdf",
                        file_name=f"{asset_name.lower().replace(' ', '_')}_rnpv_report.pdf",
                        file_bytes=rnpv_pdf,
                        mime_type="application/pdf",
                        company_name=asset_name,
                    )

                    signed_url = create_signed_report_url(storage_path)
                    st.success("Biotech PDF saved to cloud.")
                    st.link_button("Open Saved PDF", signed_url)

                except Exception as e:
                    log_exception("save_biotech_pdf_cloud", e)
                    st.error(safe_error_message())

        with excel_col:
            st.markdown('<div class="veles-mini-panel-title">Excel Model</div>', unsafe_allow_html=True)

            st.download_button(
                label="Download Banking-Style rNPV Excel Model",
                data=biotech_excel,
                file_name=f"{asset_name.lower().replace(' ', '_')}_rnpv_model.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

            if st.button("Save Excel to Cloud", key="save_biotech_excel_cloud", use_container_width=True):
                try:
                    report_id, storage_path = upload_report_bytes(
                        user_id=get_current_user()["id"],
                        report_type="biotech_rnpv_excel",
                        file_name=f"{asset_name.lower().replace(' ', '_')}_rnpv_model.xlsx",
                        file_bytes=biotech_excel,
                        mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        company_name=asset_name,
                    )

                    signed_url = create_signed_report_url(storage_path)
                    st.success("Biotech Excel model saved to cloud.")
                    st.link_button("Open Saved Excel", signed_url)

                except Exception as e:
                    log_exception("save_biotech_excel_cloud", e)
                    st.error(safe_error_message())



elif page == "Saved Models":

    page_header(
        "Saved Models",
        "Stored DCF, rNPV, and Monte Carlo valuation models."
    )

    records = list_valuations_supabase(user_id=get_current_user()["id"])

    if not records:
        activity_item(
            "No Saved Models Yet",
            "Run and save a DCF or biotech rNPV valuation to populate this page.",
            "Saved Models"
        )
    else:
        models_df = pd.DataFrame(records)

        section_title(
            "Model Library",
            "Filter and review saved valuation models."
        )

        companies = sorted(
            [
                company
                for company in models_df["company_name"].dropna().unique().tolist()
                if company
            ]
        )

        company_filter = st.selectbox(
            "Filter by company",
            ["All Companies"] + companies,
            key="saved_models_company_filter",
        )

        if company_filter != "All Companies":
            filtered_records = [
                record for record in records
                if record.get("company_name") == company_filter
            ]
        else:
            filtered_records = records

        filtered_df = pd.DataFrame(filtered_records)

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            metric_card("Saved Models", len(filtered_records), company_filter)

        with metric_col2:
            metric_card("Companies", len(companies), "Linked Models")

        with metric_col3:
            metric_card("Model Types", filtered_df["kind"].nunique() if not filtered_df.empty else 0, "Valuation Methods")

        with st.expander("View Saved Models Table", expanded=False):
            st.dataframe(filtered_df, use_container_width=True)

        if filtered_records:
            label_map = {
                f"{row['name']} | {row.get('company_name') or 'Unlinked'} | {row['kind']} | {row['created_at']}": row["id"]
                for row in filtered_records
            }

            selected_label = st.selectbox(
                "Open saved model",
                list(label_map.keys()),
                key="saved_models_open_select",
            )

            selected_id = label_map[selected_label]

            if st.button("Load Saved Model", key="saved_models_load_button"):
                record = load_valuation_supabase(
                    selected_id,
                    user_id=get_current_user()["id"],
                )

                if record:
                    section_title(
                        record.get("name", "Saved Valuation"),
                        f"Type: {record.get('kind')} | Created: {record.get('created_at')}"
                    )

                    payload = record.get("payload", {})

                    with st.expander("View Model Payload", expanded=True):
                        for key, value in payload.items():
                            st.markdown(f"### {key.replace('_', ' ').title()}")

                            if isinstance(value, list):
                                try:
                                    st.dataframe(pd.DataFrame(value), use_container_width=True)
                                except Exception:
                                    st.json(value)
                            else:
                                st.json(value)
                else:
                    st.error("Could not load valuation.")

            section_title(
                "Model Actions",
                "Open, review, or delete a saved valuation model."
            )

            delete_label = st.selectbox(
                "Select model to delete",
                list(label_map.keys()),
                key="delete_saved_model_select",
            )

            delete_id = label_map[delete_label]

            confirm_delete_model = st.checkbox(
                "I understand this will delete the selected saved model.",
                key="confirm_delete_saved_model",
            )

            if st.button("Delete Selected Model", key="delete_saved_model_button"):
                if not confirm_delete_model:
                    st.error("Confirm deletion before continuing.")
                else:
                    deleted = delete_valuation_supabase(
                        delete_id,
                        user_id=get_current_user()["id"],
                    )

                    if deleted:
                        st.success(f"Deleted model: {delete_label}")
                        st.rerun()
                    else:
                        st.error("Could not delete model.")

elif page == "Saved Reports":

    page_header(
        "Saved Reports",
        "Cloud-stored PDFs, Excel models, and signed report downloads."
    )

    try:
        reports = list_user_reports(get_current_user()["id"])

        if not reports:
            activity_item(
                "No Saved Reports Yet",
                "Save a PDF or Excel model to cloud storage to populate this page.",
                "Saved Reports"
            )
        else:
            reports_df = pd.DataFrame(reports)

            section_title(
                "Report Library",
                "Filter and open saved cloud reports."
            )

            companies = sorted(
                [
                    company
                    for company in reports_df["company_name"].dropna().unique().tolist()
                    if company
                ]
            )

            company_filter = st.selectbox(
                "Filter by company",
                ["All Companies"] + companies,
                key="saved_reports_company_filter",
            )

            if company_filter != "All Companies":
                filtered_reports = [
                    report for report in reports
                    if report.get("company_name") == company_filter
                ]
            else:
                filtered_reports = reports

            filtered_df = pd.DataFrame(filtered_reports)

            metric_col1, metric_col2, metric_col3 = st.columns(3)

            with metric_col1:
                metric_card("Saved Reports", len(filtered_reports), company_filter)

            with metric_col2:
                metric_card("Companies", len(companies), "Linked Reports")

            with metric_col3:
                storage_mb = (
                    filtered_df["file_size_bytes"].fillna(0).astype(int).sum() / (1024 * 1024)
                    if not filtered_df.empty and "file_size_bytes" in filtered_df.columns
                    else 0
                )
                metric_card("Storage", f"{storage_mb:.2f} MB", "Filtered Reports")

            with st.expander("View Saved Reports Table", expanded=False):
                st.dataframe(filtered_df, use_container_width=True)

            if filtered_reports:
                label_map = {
                    f"{row['file_name']} | {row.get('company_name') or 'Unlinked'} | {row['report_type']} | {row['created_at']}": row["storage_path"]
                    for row in filtered_reports
                }

                selected_label = st.selectbox(
                    "Open saved report",
                    list(label_map.keys()),
                    key="saved_reports_select",
                )

                if st.button("Create Signed Download Link", key="create_saved_report_signed_link", use_container_width=True):
                    signed_url = create_signed_report_url(label_map[selected_label])

                    if signed_url:
                        st.success("Signed link created.")
                        st.link_button("Open Report", signed_url, use_container_width=True)
                    else:
                        st.error("Signed URL was empty.")

    except Exception as e:
        log_exception("saved_reports_page", e)
        st.error(safe_error_message())

elif page == "Settings":

    page_header(
        "Settings",
        "Account, workspace, storage, and platform configuration."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        activity_item(
            "Account",
            "User profile, authentication state, and workspace access settings.",
            "Identity"
        )

    with col2:
        activity_item(
            "Storage",
            "Saved valuation models, PDFs, Excel exports, and cloud report usage.",
            "Files"
        )

    with col3:
        activity_item(
            "Billing",
            "Future Stripe subscription, usage limits, and invoice controls.",
            "Planned"
        )

    section_title(
        "Platform Controls",
        "Operational settings that will matter as Veles becomes an institutional product."
    )

    left, right = st.columns(2)

    with left:
        activity_item(
            "Security",
            "Audit logs, role-based permissions, rate limits, and session management will live here.",
            "Enterprise"
        )

        activity_item(
            "Data Sources",
            "Company database, research ingestion, documents, and external APIs.",
            "Research"
        )

    with right:
        activity_item(
            "Appearance",
            "Theme, density, table preferences, and analyst workspace layout.",
            "UI"
        )

        activity_item(
            "Notifications",
            "Report completion, valuation updates, watchlist alerts, and research events.",
            "Planned"
        )

elif page == "Methodology":
    st.header("Valuation Methodology")
    st.markdown(
        """
        Standard DCF estimates enterprise value by forecasting free cash flow to firm,
        discounting projected cash flows, adding terminal value, and bridging from
        enterprise value to equity value.

        Biotech rNPV will extend this by probability-adjusting cash flows based on
        clinical, regulatory, and commercialization risk.
        """
    )


if page == "Standard DCF" and "standard_dcf_outputs" in st.session_state and st.session_state.get("dcf_step_index") == 4:
    outputs = st.session_state["standard_dcf_outputs"]

    st.markdown("---")
    section_title(
        "Action Center",
        "Exports, AI memo generation, valuation storage, and cloud report management."
    )

    export_tab, memo_tab, valuation_tab, cloud_tab = st.tabs([
        "Exports",
        "AI Memo",
        "Valuation",
        "Cloud Storage",
    ])

    with export_tab:
        export_col1, export_col2 = st.columns(2)

        with export_col1:
            st.markdown("**PDF Report**")
            if "pdf" in outputs:
                st.download_button(
                    label="Download Professional DCF Report",
                    data=outputs["pdf"],
                    file_name=f"{outputs['company_name'].lower().replace(' ', '_')}_dcf_report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="action_center_download_standard_pdf",
                )
            else:
                st.info("Run the DCF model to generate a PDF export.")

        with export_col2:
            st.markdown("**Excel Model**")
            if "standard_excel" in outputs:
                st.download_button(
                    label="Download Banking-Style DCF Excel Model",
                    data=outputs["standard_excel"],
                    file_name=f"{outputs['company_name'].lower().replace(' ', '_')}_dcf_model.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                    key="action_center_download_standard_excel",
                )
            else:
                st.info("Run the DCF model to generate an Excel export.")

    with memo_tab:
        st.markdown("**AI Investment Memo**")

        if st.button("Generate AI Investment Memo", key="stable_ai_memo", use_container_width=True):
            enforce_rate_limit("standard_ai_memo", limit=10, window_seconds=3600, user_id=get_current_user()["id"])

            progress = st.progress(0)
            status = st.empty()

            try:
                status.info("Reading valuation outputs...")
                progress.progress(20)

                status.info("Analyzing forecast drivers...")
                progress.progress(40)

                status.info("Evaluating sensitivity matrix...")
                progress.progress(60)

                status.info("Building investment thesis...")
                progress.progress(80)

                memo = generate_investment_memo(
                    company_name=outputs["company_name"],
                    summary_df=outputs["summary_df"],
                    forecast_df=outputs["base_forecast"],
                    sensitivity_df=outputs["sens_df"],
                    comps_summary_df=outputs["comps_summary_df"],
                )

                st.session_state["investment_memo"] = memo

                progress.progress(100)
                status.success("Investment memo generated.")

            except Exception as e:
                log_exception("standard_ai_memo", e)
                st.error(safe_error_message())
                st.stop()

        if "investment_memo" in st.session_state:
            memo = st.session_state["investment_memo"]
            st.markdown(memo.replace('$', '\\$'))

            memo_pdf = create_dcf_pdf(
                company_name=outputs["company_name"],
                summary_df=outputs["summary_df"],
                forecast_df=outputs["base_forecast"],
                sensitivity_df=outputs["sens_df"],
                comps_df=outputs["comps_df"],
                comps_summary_df=outputs["comps_summary_df"],
                memo_text=memo,
            )

            st.session_state["standard_dcf_outputs"]["pdf"] = memo_pdf

            st.download_button(
                label="Download DCF Report With AI Memo",
                data=memo_pdf,
                file_name=f"{outputs['company_name'].lower().replace(' ', '_')}_dcf_memo_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="action_center_download_standard_memo_pdf",
            )

    with valuation_tab:
        st.markdown("**Save Standard DCF Valuation**")

        if st.button("Save Standard DCF Valuation", key="stable_save_standard_dcf", use_container_width=True):
            try:
                save_path = save_valuation_supabase(
                    valuation_type="standard_dcf",
                    name=outputs["company_name"],
                    company_name=outputs["company_name"],
                    payload={
                        "summary": outputs["summary_df"].to_dict(orient="records"),
                        "forecast": outputs["base_forecast"].to_dict(orient="records"),
                        "sensitivity": outputs["sens_df"].reset_index().to_dict(orient="records"),
                        "comparables": outputs["comps_df"].to_dict(orient="records"),
                        "comps_summary": outputs["comps_summary_df"].to_dict(orient="records"),
                    },
                    user_id=get_current_user()["id"],
                )

                st.success(f"Saved valuation: {save_path}")
            except Exception as e:
                log_exception("save_standard_dcf", e)
                st.error(safe_error_message())

    with cloud_tab:
        cloud_col1, cloud_col2 = st.columns(2)

        with cloud_col1:
            st.markdown("**PDF Cloud Storage**")
            if "pdf" in outputs:
                if st.button("Save Standard DCF PDF to Cloud", key="stable_save_standard_dcf_pdf_cloud", use_container_width=True):
                    try:
                        report_id, storage_path = upload_report_bytes(
                            user_id=get_current_user()["id"],
                            report_type="standard_dcf_pdf",
                            file_name=f"{outputs['company_name'].lower().replace(' ', '_')}_dcf_report.pdf",
                            file_bytes=outputs["pdf"],
                            mime_type="application/pdf",
                            company_name=outputs["company_name"],
                        )

                        signed_url = create_signed_report_url(storage_path)
                        st.success("Standard DCF PDF saved to cloud.")
                        st.link_button("Open Saved PDF", signed_url, use_container_width=True)

                    except Exception as e:
                        log_exception("stable_save_standard_dcf_pdf_cloud", e)
                        st.error(safe_error_message())
            else:
                st.info("No PDF available yet.")

        with cloud_col2:
            st.markdown("**Excel Cloud Storage**")
            if "standard_excel" in outputs:
                if st.button("Save Standard DCF Excel to Cloud", key="stable_save_standard_dcf_excel_cloud", use_container_width=True):
                    try:
                        report_id, storage_path = upload_report_bytes(
                            user_id=get_current_user()["id"],
                            report_type="standard_dcf_excel",
                            file_name=f"{outputs['company_name'].lower().replace(' ', '_')}_dcf_model.xlsx",
                            file_bytes=outputs["standard_excel"],
                            mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            company_name=outputs["company_name"],
                        )

                        signed_url = create_signed_report_url(storage_path)
                        st.success("Standard DCF Excel saved to cloud.")
                        st.link_button("Open Saved Excel", signed_url, use_container_width=True)

                    except Exception as e:
                        log_exception("stable_save_standard_dcf_excel_cloud", e)
                        st.error(safe_error_message())

            else:
                st.info("No Excel model available yet.")


if page == "Biotech rNPV" and "rnpv_outputs" in st.session_state:
    outputs = st.session_state["rnpv_outputs"]

    section_title(
        "AI & Research",
        "Generate an investment memo from the current biotech valuation outputs."
    )

    if st.button("Generate Biotech AI Memo", key="stable_biotech_memo", use_container_width=True):
        enforce_rate_limit("biotech_ai_memo", limit=10, window_seconds=3600, user_id=get_current_user()["id"])

        progress = st.progress(0)
        status = st.empty()

        try:
            status.info("Reading biotech valuation outputs...")
            progress.progress(20)

            status.info("Analyzing probability-adjusted forecast...")
            progress.progress(40)

            status.info("Evaluating clinical and regulatory risk...")
            progress.progress(60)

            status.info("Building biotech investment thesis...")
            progress.progress(80)

            biotech_memo = generate_biotech_memo(
                asset_name=outputs["asset_name"],
                valuation_df=outputs["valuation_df"],
                forecast_df=outputs["forecast_df"],
            )

            st.session_state["biotech_memo"] = biotech_memo

            progress.progress(100)
            status.success("Biotech valuation memo generated.")

        except Exception as e:
            log_exception("biotech_ai_memo", e)
            st.error(safe_error_message())
            st.stop()

    if "biotech_memo" in st.session_state:
        biotech_memo = st.session_state["biotech_memo"]
        st.markdown(biotech_memo.replace('$', '\\$'))

        biotech_memo_pdf = create_rnpv_pdf(
            asset_name=outputs["asset_name"],
            valuation_df=outputs["valuation_df"],
            forecast_df=outputs["forecast_df"],
            clinical_stage=outputs.get("clinical_stage"),
            memo_text=biotech_memo,
        )

        st.download_button(
            label="Download Biotech rNPV Report With AI Memo",
            data=biotech_memo_pdf,
            file_name=f"{outputs['asset_name'].lower().replace(' ', '_')}_rnpv_memo_report.pdf",
            mime="application/pdf",
        )



if page == "Biotech rNPV" and "rnpv_outputs" in st.session_state:
    outputs = st.session_state["rnpv_outputs"]

    section_title(
        "Valuation Management",
        "Store this rNPV model in the saved valuation library."
    )

    if st.button("Save Biotech rNPV Valuation", key="stable_save_biotech_rnpv", use_container_width=True):
        try:
            save_path = save_valuation_supabase(
                valuation_type="biotech_rnpv",
            name=outputs["asset_name"],
            company_name=outputs["asset_name"],
            payload={
                "clinical_stage": outputs["clinical_stage"],
                "valuation": outputs["valuation_df"].to_dict(orient="records"),
                "forecast": outputs["forecast_df"].to_dict(orient="records"),
                "sensitivity": outputs["sensitivity_df"].reset_index().to_dict(orient="records"),
                "monte_carlo_summary": outputs["monte_carlo_summary_df"].to_dict(orient="records"),
                "monte_carlo_percentiles": outputs["monte_carlo_percentile_df"].to_dict(orient="records"),
                "tornado": outputs["tornado_df"].to_dict(orient="records"),
            },
            user_id=get_current_user()["id"],
        )

            st.success(f"Saved biotech valuation: {save_path}")
        except Exception as e:
            log_exception("save_biotech_rnpv", e)
            st.error(safe_error_message())




# =========================
# Veles Company Data Layer Test
# =========================
try:
    import streamlit as st
    from services.equity_report_engine import build_equity_report_from_ticker_v2
    from services.pdf_report_exporter import export_equity_report_pdf_v2

    st.divider()
    st.header("Veles Company Data Layer")
    st.caption("Generate a report directly from a ticker using the internal company data service.")

    with st.form("veles_company_data_layer_form"):
        ticker_input = st.text_input("Ticker Symbol", "RXRX")
        package_input = st.selectbox(
            "Report Package",
            ["Basic", "Professional"],
            index=0,
        )
        data_layer_submitted = st.form_submit_button(
            "Generate Report From Ticker"
        )

    if data_layer_submitted:
        data_report = build_equity_report_from_ticker_v2(
            ticker_input,
            package=package_input,
        )
        data_output_path = f"reports/generated/{ticker_input.lower()}_data_layer_report.pdf"
        data_pdf_path = export_equity_report_pdf_v2(data_report, data_output_path)

        st.success("Ticker-based report generated successfully.")
        st.write(f"Saved to: `{data_pdf_path}`")

        with open(data_pdf_path, "rb") as f:
            st.download_button(
                label="Download Data Layer Report",
                data=f,
                file_name=f"{ticker_input.lower()}_data_layer_report.pdf",
                mime="application/pdf",
            )

except Exception as e:
    st.error(f"Company data layer failed: {e}")
