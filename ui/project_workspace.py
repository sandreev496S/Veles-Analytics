from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

from services.crm import (
    CRMProject,
    ChecklistCompletionError,
    add_task,
    checklist_summary,
    add_timeline_event,
    delete_task,
    delete_workspace_file,
    list_tasks,
    list_timeline_events,
    list_workspace_files,
    load_checklist,
    load_research_notes,
    pull_sec_and_financial_data,
    record_project_event,
    save_deliverable,
    save_project_upload,
    save_research_notes,
    set_checklist_item,
    update_project,
    validate_project_completion,
    update_task_status,
)


NOTE_SECTIONS = [
    "Investment Thesis",
    "Bull Case",
    "Bear Case",
    "Key Catalysts",
    "Key Risks",
    "Business Model",
    "Financial Position",
    "Clinical Pipeline",
    "Partnerships",
    "Competitive Position",
    "Valuation Notes",
    "Questions to Investigate",
]


def _project_health(
    project: CRMProject,
) -> dict[str, str]:
    summary = checklist_summary(project)
    progress = summary["progress_percent"]

    if progress >= 90:
        return {
            "label": "Healthy",
            "tone": "green",
            "description": (
                "The project is close to completion "
                "with few required items remaining."
            ),
        }

    if progress >= 60:
        return {
            "label": "Needs Attention",
            "tone": "orange",
            "description": (
                "The project is progressing, but "
                "required checklist items remain."
            ),
        }

    return {
        "label": "At Risk",
        "tone": "red",
        "description": (
            "Several required project controls "
            "remain incomplete."
        ),
    }


def _completion_checklist(
    project: CRMProject,
) -> None:
    st.subheader("Project Completion Checklist")

    checklist = load_checklist(project)
    summary = checklist_summary(project)
    health = _project_health(project)

    metric_col1, metric_col2, metric_col3 = st.columns(3)

    metric_col1.metric(
        "Required Progress",
        f"{summary['progress_percent']}%",
    )

    metric_col2.metric(
        "Required Items",
        (
            f"{summary['completed_required_items']} / "
            f"{summary['required_items']}"
        ),
    )

    metric_col3.metric(
        "Project Health",
        health["label"],
    )

    st.progress(
        summary["progress"]
    )

    st.caption(
        health["description"]
    )

    categories: dict[str, list[dict]] = {}

    for item in checklist.get("items", []):
        category = str(
            item.get("category", "General")
        )

        categories.setdefault(
            category,
            [],
        ).append(item)

    for category, items in categories.items():
        st.markdown(f"### {category}")

        with st.container(border=True):
            for item in items:
                item_id = str(item["id"])
                required = bool(
                    item.get("required")
                )
                automatic = bool(
                    item.get("automatic")
                )

                label_suffix = (
                    " — Required"
                    if required
                    else " — Optional"
                )

                if automatic:
                    label_suffix += " · Auto"

                current_value = bool(
                    item.get("completed")
                )

                selected_value = st.checkbox(
                    (
                        f"{item.get('title', item_id)}"
                        f"{label_suffix}"
                    ),
                    value=current_value,
                    key=(
                        f"project_checklist_"
                        f"{project.project_id}_"
                        f"{item_id}"
                    ),
                    disabled=automatic,
                )

                if (
                    not automatic
                    and selected_value
                    != current_value
                ):
                    set_checklist_item(
                        project,
                        item_id=item_id,
                        completed=selected_value,
                    )

                    st.rerun()

    incomplete = summary[
        "incomplete_required_items"
    ]

    st.markdown("### Completion Readiness")

    if not incomplete:
        st.success(
            "All required checklist items are complete. "
            "The project may be marked Completed."
        )
    else:
        st.warning(
            f"{len(incomplete)} required item(s) "
            "remain before this project can be completed."
        )

        for item in incomplete:
            st.write(
                f"• {item.get('title', item.get('id'))}"
            )


def _overview(
    project: CRMProject,
) -> None:
    st.subheader(
        f"{project.company_name} Project"
    )

    st.caption(
        f"{project.project_id} · "
        f"{project.client_name}"
    )

    completion = checklist_summary(project)
    health = _project_health(project)

    metrics = st.columns(7)

    metrics[0].metric(
        "Status",
        project.status,
    )
    metrics[1].metric(
        "Package",
        project.package,
    )
    metrics[2].metric(
        "Due Date",
        project.due_date or "Not set",
    )
    metrics[3].metric(
        "Priority",
        project.priority,
    )
    metrics[4].metric(
        "Progress",
        f"{completion['progress_percent']}%",
    )
    metrics[5].metric(
        "Health",
        health["label"],
    )
    metrics[6].metric(
        "Price",
        f"${project.price_usd:,.2f}",
    )

    st.progress(
        completion["progress"]
    )

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown("#### Project Brief")

        st.write(
            project.primary_objective
            or "No project objective recorded."
        )

        st.markdown("**Intended audience**")
        st.write(
            project.intended_audience
            or "Not specified"
        )

        st.markdown("**Requested deliverables**")
        st.write(
            project.requested_deliverables
            or "Not specified"
        )

        st.markdown("**Requested focus areas**")
        st.write(
            project.requested_focus_areas
            or "Not specified"
        )

    with right:
        st.markdown("#### Data Status")

        st.write(
            f"**Source mode:** "
            f"{project.data_source_mode}"
        )
        st.write(
            f"**SEC data:** "
            f"{project.sec_data_status}"
        )
        st.write(
            f"**Financial data:** "
            f"{project.financial_data_status}"
        )
        st.write(
            f"**Payment:** "
            f"{project.payment_status}"
        )

        if project.folder_path:
            st.markdown("**Workspace folder**")
            st.code(
                project.folder_path,
                language=None,
            )

    st.markdown("#### Update Project")

    with st.form(
        f"workspace_update_{project.project_id}"
    ):
        col1, col2, col3 = st.columns(3)

        status = col1.selectbox(
            "Status",
            [
                "Lead",
                "In Progress",
                "Waiting on Client",
                "Quality Control",
                "Delivered",
                "Completed",
                "Archived",
            ],
            index=(
                [
                    "Lead",
                    "In Progress",
                    "Waiting on Client",
                    "Quality Control",
                    "Delivered",
                    "Completed",
                    "Archived",
                ].index(project.status)
                if project.status
                in [
                    "Lead",
                    "In Progress",
                    "Waiting on Client",
                    "Quality Control",
                    "Delivered",
                    "Completed",
                    "Archived",
                ]
                else 0
            ),
        )

        priority = col2.selectbox(
            "Priority",
            [
                "Low",
                "Medium",
                "High",
                "Urgent",
            ],
            index=(
                [
                    "Low",
                    "Medium",
                    "High",
                    "Urgent",
                ].index(project.priority)
                if project.priority
                in [
                    "Low",
                    "Medium",
                    "High",
                    "Urgent",
                ]
                else 1
            ),
        )

        payment_status = col3.selectbox(
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

        notes = st.text_area(
            "Internal Notes",
            value=project.notes,
        )

        submitted = st.form_submit_button(
            "Save Project Updates",
            use_container_width=True,
        )

    if submitted:
        if (
            status == "Completed"
            and project.status != "Completed"
        ):
            try:
                validate_project_completion(
                    project
                )
            except ChecklistCompletionError as exc:
                st.error(str(exc))
                return

        updated = update_project(
            project.project_id,
            {
                "status": status,
                "priority": priority,
                "payment_status": payment_status,
                "hours_worked": hours_worked,
                "revision_count": revision_count,
                "notes": notes,
            },
        )

        add_timeline_event(
            updated,
            event_type="project_updated",
            title="Project details updated",
        )

        if (
            payment_status == "Paid"
            and project.payment_status != "Paid"
        ):
            record_project_event(
                updated,
                "payment_confirmed",
                description=(
                    "Project payment status changed "
                    "to Paid."
                ),
            )

        st.success("Project updated.")
        st.rerun()


def _files(
    project: CRMProject,
) -> None:
    st.subheader("Project Files")

    upload_col, list_col = st.columns(
        [0.85, 1.35]
    )

    with upload_col:
        document_type = st.selectbox(
            "Document Type",
            [
                "Client Upload",
                "SEC Filing",
                "Financial Statement",
                "Research Document",
            ],
            key=(
                f"workspace_document_type_"
                f"{project.project_id}"
            ),
        )

        description = st.text_input(
            "Source or Description",
            key=(
                f"workspace_document_note_"
                f"{project.project_id}"
            ),
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
                "pptx",
            ],
            key=(
                f"workspace_upload_"
                f"{project.project_id}"
            ),
        )

        if st.button(
            "Save Files",
            key=(
                f"workspace_save_files_"
                f"{project.project_id}"
            ),
            use_container_width=True,
        ):
            if not files:
                st.warning(
                    "Select at least one file."
                )
            else:
                for uploaded in files:
                    save_project_upload(
                        project=project,
                        filename=uploaded.name,
                        data=uploaded.getvalue(),
                        document_type=document_type,
                        source_note=description,
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

                event_type = {
                    "Client Upload": (
                        "client_document_uploaded"
                    ),
                    "SEC Filing": (
                        "sec_filing_uploaded"
                    ),
                    "Financial Statement": (
                        "financial_statement_uploaded"
                    ),
                    "Research Document": (
                        "client_document_uploaded"
                    ),
                }.get(
                    document_type,
                    "client_document_uploaded",
                )

                record_project_event(
                    project,
                    event_type,
                    description=(
                        f"{len(files)} file(s) saved as "
                        f"{document_type}."
                    ),
                    metadata={
                        "file_count": len(files),
                        "document_type": document_type,
                        "filenames": [
                            uploaded.name
                            for uploaded in files
                        ],
                    },
                )

                st.success(
                    f"Saved {len(files)} file(s)."
                )
                st.rerun()

    with list_col:
        rows = list_workspace_files(project)

        if not rows:
            st.info(
                "No project files have been saved."
            )
        else:
            dataframe = pd.DataFrame(rows)

            st.dataframe(
                dataframe[
                    [
                        "category",
                        "filename",
                        "size_bytes",
                        "modified_at",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )

            file_map = {
                (
                    f"{row['category']} — "
                    f"{row['filename']}"
                ): row["path"]
                for row in rows
            }

            selected_label = st.selectbox(
                "Select File",
                list(file_map),
                key=(
                    f"workspace_file_select_"
                    f"{project.project_id}"
                ),
            )

            selected_path = Path(
                file_map[selected_label]
            )

            action_col1, action_col2 = (
                st.columns(2)
            )

            with action_col1:
                if selected_path.exists():
                    st.download_button(
                        "Download Selected File",
                        data=selected_path.read_bytes(),
                        file_name=selected_path.name,
                        use_container_width=True,
                        key=(
                            f"workspace_download_"
                            f"{project.project_id}"
                        ),
                    )

            with action_col2:
                if st.button(
                    "Delete Selected File",
                    use_container_width=True,
                    key=(
                        f"workspace_delete_file_"
                        f"{project.project_id}"
                    ),
                ):
                    delete_workspace_file(
                        project,
                        str(selected_path),
                    )
                    st.success("File deleted.")
                    st.rerun()


def _company_data(
    project: CRMProject,
) -> None:
    st.subheader("SEC and Financial Data")

    st.write(
        "Use Veles providers for a public company "
        "or upload client-supplied documents in "
        "the Files tab."
    )

    if not project.ticker:
        st.warning(
            "Add a ticker to the project before "
            "using automatic data pulls."
        )
        return

    pull_sec = st.checkbox(
        "Pull SEC filings and company facts",
        value=True,
        key=(
            f"workspace_pull_sec_"
            f"{project.project_id}"
        ),
    )

    pull_financials = st.checkbox(
        "Pull financial statements and market data",
        value=True,
        key=(
            f"workspace_pull_financials_"
            f"{project.project_id}"
        ),
    )

    use_cache = st.checkbox(
        "Use cached provider data when available",
        value=True,
        key=(
            f"workspace_use_cache_"
            f"{project.project_id}"
        ),
    )

    if st.button(
        "Pull Company Data",
        use_container_width=True,
        key=(
            f"workspace_pull_data_"
            f"{project.project_id}"
        ),
    ):
        try:
            with st.spinner(
                "Pulling and storing company data..."
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

            capabilities = result.get(
                "capabilities",
                [],
            )

            if pull_sec:
                record_project_event(
                    project,
                    "sec_data_pulled",
                    description=(
                        f"SEC data pulled for "
                        f"{project.ticker.upper()}."
                    ),
                    metadata={
                        "capabilities": capabilities,
                    },
                )

            if pull_financials:
                record_project_event(
                    project,
                    "financial_data_pulled",
                    description=(
                        f"Financial and market data "
                        f"pulled for "
                        f"{project.ticker.upper()}."
                    ),
                    metadata={
                        "capabilities": capabilities,
                    },
                )

            st.success(
                "Company data saved to the "
                "project workspace."
            )

            for written_file in result.get(
                "written_files",
                [],
            ):
                st.code(
                    written_file,
                    language=None,
                )

        except Exception as exc:
            st.exception(exc)

    rows = [
        row
        for row in list_workspace_files(
            project
        )
        if row["category"]
        in {
            "SEC Data",
            "Financial Data",
        }
    ]

    if rows:
        st.markdown(
            "#### Stored Company Data"
        )

        st.dataframe(
            pd.DataFrame(rows),
            use_container_width=True,
            hide_index=True,
        )


def _research_notes(
    project: CRMProject,
) -> None:
    st.subheader("Research Notes")

    existing = load_research_notes(
        project
    )

    with st.form(
        f"workspace_notes_{project.project_id}"
    ):
        notes: dict[str, str] = {}

        for section in NOTE_SECTIONS:
            notes[section] = st.text_area(
                section,
                value=existing.get(
                    section,
                    "",
                ),
                height=110,
            )

        submitted = st.form_submit_button(
            "Save Research Notes",
            use_container_width=True,
        )

    if submitted:
        save_research_notes(
            project,
            notes,
        )

        record_project_event(
            project,
            "research_notes_saved",
            description=(
                "Project research notes were updated."
            ),
            metadata={
                "populated_sections": [
                    section
                    for section, value
                    in notes.items()
                    if value.strip()
                ],
            },
        )

        st.success(
            "Research notes saved."
        )


def _tasks(
    project: CRMProject,
) -> None:
    st.subheader("Project Tasks")

    with st.form(
        f"workspace_task_form_"
        f"{project.project_id}"
    ):
        task_title = st.text_input(
            "Task Title"
        )

        task_description = st.text_area(
            "Task Description"
        )

        col1, col2 = st.columns(2)

        priority = col1.selectbox(
            "Priority",
            [
                "Low",
                "Medium",
                "High",
                "Urgent",
            ],
            index=1,
        )

        due_date = col2.date_input(
            "Due Date",
            value=date.today(),
        )

        submitted = st.form_submit_button(
            "Add Task",
            use_container_width=True,
        )

    if submitted:
        if not task_title.strip():
            st.error(
                "Enter a task title."
            )
        else:
            add_task(
                project,
                title=task_title,
                description=task_description,
                priority=priority,
                due_date=due_date.isoformat(),
            )

            st.success("Task created.")
            st.rerun()

    tasks = list_tasks(project)

    if not tasks:
        st.info(
            "No tasks have been created."
        )
        return

    status_order = {
        "Open": 0,
        "In Progress": 1,
        "Completed": 2,
    }

    tasks = sorted(
        tasks,
        key=lambda task: (
            status_order.get(
                task.get("status", ""),
                99,
            ),
            task.get("due_date", ""),
        ),
    )

    for task in tasks:
        with st.container(border=True):
            col1, col2, col3 = st.columns(
                [2.5, 1, 1]
            )

            col1.markdown(
                f"**{task['title']}**"
            )

            if task.get("description"):
                col1.caption(
                    task["description"]
                )

            col1.caption(
                f"Priority: {task['priority']} · "
                f"Due: {task['due_date'] or 'Not set'}"
            )

            status_options = [
                "Open",
                "In Progress",
                "Completed",
            ]

            current_status = task.get(
                "status",
                "Open",
            )

            selected_status = col2.selectbox(
                "Status",
                status_options,
                index=(
                    status_options.index(
                        current_status
                    )
                    if current_status
                    in status_options
                    else 0
                ),
                key=(
                    f"task_status_"
                    f"{task['task_id']}"
                ),
                label_visibility="collapsed",
            )

            if selected_status != current_status:
                update_task_status(
                    project,
                    task_id=task["task_id"],
                    status=selected_status,
                )
                st.rerun()

            if col3.button(
                "Delete",
                key=(
                    f"task_delete_"
                    f"{task['task_id']}"
                ),
                use_container_width=True,
            ):
                delete_task(
                    project,
                    task["task_id"],
                )
                st.rerun()


def _timeline(
    project: CRMProject,
) -> None:
    st.subheader("Activity Timeline")

    events = list_timeline_events(
        project
    )

    if not events:
        st.info(
            "No project activity has been recorded."
        )
        return

    for event in events:
        timestamp = pd.to_datetime(
            event.get("timestamp"),
            errors="coerce",
        )

        formatted_time = (
            timestamp.strftime(
                "%b %d, %Y · %I:%M %p"
            )
            if not pd.isna(timestamp)
            else event.get(
                "timestamp",
                "",
            )
        )

        with st.container(border=True):
            st.markdown(
                f"**{event.get('title', 'Activity')}**"
            )
            st.caption(
                f"{formatted_time} · "
                f"{event.get('event_type', 'event')}"
            )

            if event.get("description"):
                st.write(
                    event["description"]
                )


def _deliverables(
    project: CRMProject,
) -> None:
    st.subheader("Deliverables")

    description = st.text_input(
        "Deliverable Description",
        key=(
            f"deliverable_description_"
            f"{project.project_id}"
        ),
    )

    files = st.file_uploader(
        "Upload Final Deliverables",
        accept_multiple_files=True,
        type=[
            "pdf",
            "xlsx",
            "xls",
            "csv",
            "docx",
            "pptx",
            "zip",
        ],
        key=(
            f"deliverable_upload_"
            f"{project.project_id}"
        ),
    )

    if st.button(
        "Save Deliverables",
        use_container_width=True,
        key=(
            f"save_deliverables_"
            f"{project.project_id}"
        ),
    ):
        if not files:
            st.warning(
                "Select at least one deliverable."
            )
        else:
            for uploaded in files:
                save_deliverable(
                    project,
                    filename=uploaded.name,
                    data=uploaded.getvalue(),
                    description=description,
                )

            st.success(
                f"Saved {len(files)} "
                "deliverable(s)."
            )
            st.rerun()

    deliverables = [
        row
        for row in list_workspace_files(
            project
        )
        if row["category"]
        == "Final Deliverables"
    ]

    if deliverables:
        st.dataframe(
            pd.DataFrame(deliverables),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("#### Client Delivery Status")

    if st.button(
        "Mark Client as Notified",
        use_container_width=True,
        key=(
            f"client_notified_"
            f"{project.project_id}"
        ),
    ):
        record_project_event(
            project,
            "client_notified",
            description=(
                "Client delivery notification was "
                "recorded."
            ),
        )

        st.success(
            "Client notification recorded."
        )
        st.rerun()


def render_project_workspace(
    project: CRMProject,
) -> None:
    st.markdown(
        f"## {project.company_name}"
    )

    st.caption(
        f"{project.project_id} · "
        f"{project.client_name} · "
        f"{project.package}"
    )

    tabs = st.tabs([
        "Overview",
        "Completion Checklist",
        "Files",
        "Company Data",
        "Research Notes",
        "Tasks",
        "Timeline",
        "Deliverables",
    ])

    with tabs[0]:
        _overview(project)

    with tabs[1]:
        _completion_checklist(project)

    with tabs[2]:
        _files(project)

    with tabs[3]:
        _company_data(project)

    with tabs[4]:
        _research_notes(project)

    with tabs[5]:
        _tasks(project)

    with tabs[6]:
        _timeline(project)

    with tabs[7]:
        _deliverables(project)
