from __future__ import annotations

import pandas as pd
import streamlit as st


DEFAULT_COLUMNS = [
    "project_id",
    "client_name",
    "company_name",
    "ticker",
    "package",
    "status",
    "priority",
    "due_date",
    "deadline_status",
    "days_remaining",
    "price_usd",
    "payment_status",
]


COLUMN_LABELS = {
    "project_id": "Project ID",
    "client_name": "Client",
    "company_name": "Company",
    "ticker": "Ticker",
    "package": "Package",
    "status": "Status",
    "priority": "Priority",
    "due_date": "Due Date",
    "deadline_status": "Deadline",
    "days_remaining": "Days Remaining",
    "price_usd": "Price",
    "payment_status": "Payment",
}


def render_project_table(
    dataframe: pd.DataFrame,
    *,
    title: str = "Projects",
    key: str = "crm_project_table",
) -> None:
    st.markdown(f"### {title}")

    if dataframe.empty:
        st.info(
            "No projects match the current filters."
        )
        return

    visible_columns = [
        column
        for column in DEFAULT_COLUMNS
        if column in dataframe.columns
    ]

    display = dataframe[
        visible_columns
    ].copy()

    display = display.rename(
        columns=COLUMN_LABELS
    )

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        key=key,
        column_config={
            "Price": st.column_config.NumberColumn(
                format="$%.2f",
            ),
            "Days Remaining": (
                st.column_config.NumberColumn(
                    format="%d",
                )
            ),
        },
    )


def render_deadline_table(
    dataframe: pd.DataFrame,
    *,
    key: str = "crm_deadline_table",
) -> None:
    st.markdown("### Projects Requiring Attention")

    if dataframe.empty:
        st.success(
            "No active projects are overdue "
            "or due within three days."
        )
        return

    columns = [
        column
        for column in [
            "project_id",
            "client_name",
            "company_name",
            "ticker",
            "priority",
            "due_date",
            "deadline_status",
            "days_remaining",
        ]
        if column in dataframe.columns
    ]

    display = dataframe[
        columns
    ].copy().rename(
        columns=COLUMN_LABELS
    )

    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        key=key,
    )
