from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from ui.project_workspace import render_project_workspace
from components.crm.project_table import (
    render_deadline_table,
    render_project_table,
)
from components.crm.search_bar import (
    render_project_search_bar,
)
from services.crm import (
    CRMProject,
    add_deadline_columns,
    apply_project_filters,
    calculate_dashboard_metrics,
    due_projects,
    create_project,
    export_master_crm,
    get_project,
    list_project_documents,
    load_projects,
    next_project_id,
    pull_sec_and_financial_data,
    save_project_upload,
    update_project,
)


STATUS_OPTIONS = [
    "Lead",
    "In Progress",
    "Waiting on Client",
    "Quality Control",
    "Delivered",
    "Completed",
    "Archived",
]

PACKAGE_OPTIONS = [
    "Basic",
    "Standard",
    "Premium",
    "Custom",
]

PROJECT_TYPES = [
    "Equity Research",
    "Financial Modeling",
    "SEC Filing Review",
    "Competitive Analysis",
    "Biotechnology Intelligence",
    "Custom Research",
]

PRIORITY_OPTIONS = [
    "Low",
    "Medium",
    "High",
    "Urgent",
]


def _project_dataframe() -> pd.DataFrame:
    projects = load_projects()

    rows = []

    for project in projects:
        row = project.to_dict()
        row["effective_hourly_rate"] = (
            project.effective_hourly_rate
        )

        rows.append(row)

    return pd.DataFrame(rows)


def _overview() -> None:
    dataframe = _project_dataframe()

    if dataframe.empty:
        st.info(
            "No CRM projects have been created yet."
        )
        return

    dataframe = add_deadline_columns(
        dataframe
    )

    filter_values = render_project_search_bar(
        dataframe,
        key_prefix="crm_overview",
    )

    filtered = apply_project_filters(
        dataframe,
        **filter_values,
    )

    metrics = calculate_dashboard_metrics(
        filtered
    )

    metric_columns = st.columns(6)

    metric_columns[0].metric(
        "Projects",
        metrics["total_projects"],
    )
    metric_columns[1].metric(
        "Active",
        metrics["active_projects"],
    )
    metric_columns[2].metric(
        "Due Soon",
        metrics["due_this_week"],
    )
    metric_columns[3].metric(
        "Overdue",
        metrics["overdue_projects"],
    )
    metric_columns[4].metric(
        "Paid Revenue",
        f"${metrics['paid_revenue']:,.2f}",
    )
    metric_columns[5].metric(
        "Outstanding",
        (
            f"${metrics['outstanding_revenue']:,.2f}"
        ),
    )

    attention_projects = due_projects(
        filtered
    )

    render_deadline_table(
        attention_projects,
        key="crm_attention_projects",
    )

    render_project_table(
        filtered,
        title=(
            f"Project Directory "
            f"({len(filtered)} results)"
        ),
        key="crm_filtered_projects",
    )



def _new_project() -> None:
    projects = load_projects()
    generated_id = next_project_id(projects)

    with st.form("crm_new_project"):
        st.subheader("Client and Project Details")

        col1, col2 = st.columns(2)

        project_id = col1.text_input(
            "Project ID",
            value=generated_id,
        )

        client_name = col2.text_input(
            "Client Name *"
        )

        company_name = col1.text_input(
            "Company Name *"
        )

        ticker = col2.text_input(
            "Ticker"
        ).upper()

        client_email = col1.text_input(
            "Client Email"
        )

        country = col2.text_input(
            "Country"
        )

        industry = col1.text_input(
            "Industry"
        )

        company_website = col2.text_input(
            "Company Website"
        )

        package = col1.selectbox(
            "Package",
            PACKAGE_OPTIONS,
        )

        project_type = col2.selectbox(
            "Project Type",
            PROJECT_TYPES,
        )

        status = col1.selectbox(
            "Status",
            STATUS_OPTIONS,
            index=1,
        )

        priority = col2.selectbox(
            "Priority",
            PRIORITY_OPTIONS,
            index=1,
        )

        order_date = col1.date_input(
            "Order Date",
            value=date.today(),
        )

        due_date = col2.date_input(
            "Due Date",
            value=date.today(),
        )

        price_usd = col1.number_input(
            "Price (USD)",
            min_value=0.0,
            step=25.0,
        )

        lead_source = col2.selectbox(
            "Lead Source",
            [
                "Fiverr",
                "Website",
                "Referral",
                "LinkedIn",
                "Direct",
            ],
        )

        primary_objective = st.text_area(
            "Primary Objective"
        )

        intended_audience = st.text_input(
            "Intended Audience"
        )

        requested_deliverables = st.text_area(
            "Requested Deliverables"
        )

        requested_focus_areas = st.text_area(
            "Requested Focus Areas"
        )

        notes = st.text_area("Notes")

        submitted = st.form_submit_button(
            "Create Project",
            use_container_width=True,
        )

    if not submitted:
        return

    if not client_name or not company_name:
        st.error(
            "Client name and company name are required."
        )
        return

    project = CRMProject(
        project_id=project_id,
        client_name=client_name,
        company_name=company_name,
        ticker=ticker,
        industry=industry,
        country=country,
        client_email=client_email,
        company_website=company_website,
        lead_source=lead_source,
        package=package,
        project_type=project_type,
        status=status,
        priority=priority,
        order_date=order_date.isoformat(),
        due_date=due_date.isoformat(),
        price_usd=price_usd,
        primary_objective=(
            primary_objective
        ),
        intended_audience=(
            intended_audience
        ),
        requested_deliverables=(
            requested_deliverables
        ),
        requested_focus_areas=(
            requested_focus_areas
        ),
        notes=notes,
    )

    created = create_project(project)

    st.success(
        f"Created {created.project_id}"
    )
    st.code(created.folder_path)


def _project_management() -> None:
    projects = load_projects()

    if not projects:
        st.info("Create a project first.")
        return

    project_map = {
        (
            f"{project.project_id} — "
            f"{project.client_name} — "
            f"{project.company_name}"
        ): project.project_id
        for project in projects
    }

    selected_label = st.selectbox(
        "Select Project",
        list(project_map),
    )

    project_id = project_map[selected_label]
    project = get_project(project_id)

    if project is None:
        st.error("Project could not be loaded.")
        return

    st.caption(project.folder_path)

    tab_details, tab_documents, tab_data = st.tabs([
        "Project Details",
        "Documents",
        "SEC and Financial Data",
    ])

    with tab_details:
        with st.form(
            f"edit_{project.project_id}"
        ):
            col1, col2 = st.columns(2)

            status = col1.selectbox(
                "Status",
                STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(
                    project.status
                )
                if project.status
                in STATUS_OPTIONS
                else 0,
            )

            priority = col2.selectbox(
                "Priority",
                PRIORITY_OPTIONS,
                index=PRIORITY_OPTIONS.index(
                    project.priority
                )
                if project.priority
                in PRIORITY_OPTIONS
                else 1,
            )

            hours_worked = col1.number_input(
                "Hours Worked",
                min_value=0.0,
                value=float(
                    project.hours_worked
                ),
                step=0.5,
            )

            revision_count = col2.number_input(
                "Revision Count",
                min_value=0,
                value=int(
                    project.revision_count
                ),
            )

            payment_status = col1.selectbox(
                "Payment Status",
                [
                    "Pending",
                    "Paid",
                    "Partially Paid",
                    "Refunded",
                ],
                index=(
                    [
                        "Pending",
                        "Paid",
                        "Partially Paid",
                        "Refunded",
                    ].index(
                        project.payment_status
                    )
                    if project.payment_status
                    in [
                        "Pending",
                        "Paid",
                        "Partially Paid",
                        "Refunded",
                    ]
                    else 0
                ),
            )

            client_rating = col2.number_input(
                "Client Rating",
                min_value=0.0,
                max_value=5.0,
                value=float(
                    project.client_rating or 0
                ),
                step=0.5,
            )

            notes = st.text_area(
                "Notes",
                value=project.notes,
            )

            update_clicked = (
                st.form_submit_button(
                    "Save Project Changes",
                    use_container_width=True,
                )
            )

        if update_clicked:
            updated = update_project(
                project.project_id,
                {
                    "status": status,
                    "priority": priority,
                    "hours_worked": (
                        hours_worked
                    ),
                    "revision_count": (
                        revision_count
                    ),
                    "payment_status": (
                        payment_status
                    ),
                    "client_rating": (
                        client_rating
                        if client_rating > 0
                        else None
                    ),
                    "notes": notes,
                },
            )

            st.success(
                f"Updated {updated.project_id}"
            )

    with tab_documents:
        document_type = st.selectbox(
            "Document Type",
            [
                "Client Upload",
                "SEC Filing",
                "Financial Statement",
                "Research Document",
            ],
        )

        source_note = st.text_input(
            "Source or Description"
        )

        files = st.file_uploader(
            "Upload Files",
            accept_multiple_files=True,
            type=[
                "pdf",
                "xlsx",
                "xls",
                "csv",
                "docx",
                "txt",
                "json",
            ],
        )

        if st.button(
            "Save Uploaded Files",
            use_container_width=True,
        ):
            if not files:
                st.warning(
                    "Select at least one file."
                )
            else:
                saved_paths = []

                for uploaded_file in files:
                    saved_path = save_project_upload(
                        project=project,
                        filename=(
                            uploaded_file.name
                        ),
                        data=uploaded_file.getvalue(),
                        document_type=(
                            document_type
                        ),
                        source_note=source_note,
                    )

                    saved_paths.append(
                        str(saved_path)
                    )

                updates = {
                    "data_source_mode": (
                        "Client/manual uploads"
                    ),
                }

                if document_type == "SEC Filing":
                    updates[
                        "sec_data_status"
                    ] = "Uploaded"

                if (
                    document_type
                    == "Financial Statement"
                ):
                    updates[
                        "financial_data_status"
                    ] = "Uploaded"

                update_project(
                    project.project_id,
                    updates,
                )

                st.success(
                    f"Saved {len(saved_paths)} "
                    "file(s)."
                )

                for path in saved_paths:
                    st.code(path)

        documents = list_project_documents(
            project
        )

        if documents:
            st.dataframe(
                pd.DataFrame(documents),
                use_container_width=True,
                hide_index=True,
            )

    with tab_data:
        st.write(
            "Pull normalized SEC and financial "
            "data using the existing Veles "
            "providers."
        )

        pull_sec = st.checkbox(
            "Pull SEC filings and company facts",
            value=True,
        )

        pull_financials = st.checkbox(
            "Pull financial statements and market data",
            value=True,
        )

        use_cache = st.checkbox(
            "Use provider cache when available",
            value=True,
        )

        if st.button(
            "Pull Project Data",
            use_container_width=True,
        ):
            try:
                with st.spinner(
                    "Pulling project data..."
                ):
                    result = (
                        pull_sec_and_financial_data(
                            project,
                            pull_sec=pull_sec,
                            pull_financials=(
                                pull_financials
                            ),
                            use_cache=use_cache,
                        )
                    )

                st.success(
                    "Project data saved."
                )

                for written_file in result[
                    "written_files"
                ]:
                    st.code(written_file)

            except Exception as exc:
                st.exception(exc)


def _export() -> None:
    st.write(
        "Generate an Excel master CRM containing "
        "every project and client."
    )

    if st.button(
        "Generate Master CRM Workbook",
        use_container_width=True,
    ):
        output = export_master_crm()

        st.success(
            f"Created {output.name}"
        )

        st.download_button(
            "Download Master CRM",
            data=output.read_bytes(),
            file_name=output.name,
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
            use_container_width=True,
        )


def render_crm_page() -> None:
    st.title("Veles Operations CRM")
    st.caption(
        "Manage clients, projects, source documents, "
        "deadlines, payments, and data collection."
    )

    tabs = st.tabs([
        "Overview",
        "New Project",
        "Project Workspace",
        "Manage Projects",
        "Export CRM",
    ])

    with tabs[0]:
        _overview()

    with tabs[1]:
        _new_project()

    with tabs[2]:
        projects = load_projects()

        if not projects:
            st.info(
                "Create a project before opening "
                "a project workspace."
            )
        else:
            project_map = {
                (
                    f"{project.project_id} — "
                    f"{project.client_name} — "
                    f"{project.company_name}"
                ): project
                for project in projects
            }

            selected_project_label = st.selectbox(
                "Open Project Workspace",
                list(project_map),
                key="crm_workspace_project_select",
            )

            render_project_workspace(
                project_map[
                    selected_project_label
                ]
            )

    with tabs[3]:
        _project_management()

    with tabs[4]:
        _export()
