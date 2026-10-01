from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from services.crm.search import (
    unique_filter_options,
)


def render_project_search_bar(
    dataframe: pd.DataFrame,
    *,
    key_prefix: str = "crm",
) -> dict[str, Any]:
    st.markdown("### Search and Filters")

    search_query = st.text_input(
        "Search projects",
        placeholder=(
            "Search client, company, ticker, "
            "project ID, objective, or notes"
        ),
        key=f"{key_prefix}_search_query",
    )

    row1 = st.columns(3)
    row2 = st.columns(3)

    statuses = row1[0].multiselect(
        "Status",
        unique_filter_options(
            dataframe,
            "status",
        ),
        key=f"{key_prefix}_status_filter",
    )

    packages = row1[1].multiselect(
        "Package",
        unique_filter_options(
            dataframe,
            "package",
        ),
        key=f"{key_prefix}_package_filter",
    )

    priorities = row1[2].multiselect(
        "Priority",
        unique_filter_options(
            dataframe,
            "priority",
        ),
        key=f"{key_prefix}_priority_filter",
    )

    payment_statuses = row2[0].multiselect(
        "Payment",
        unique_filter_options(
            dataframe,
            "payment_status",
        ),
        key=f"{key_prefix}_payment_filter",
    )

    lead_sources = row2[1].multiselect(
        "Lead Source",
        unique_filter_options(
            dataframe,
            "lead_source",
        ),
        key=f"{key_prefix}_lead_filter",
    )

    deadline_statuses = row2[2].multiselect(
        "Deadline",
        unique_filter_options(
            dataframe,
            "deadline_status",
        ),
        key=f"{key_prefix}_deadline_filter",
    )

    return {
        "search_query": search_query,
        "statuses": statuses,
        "packages": packages,
        "priorities": priorities,
        "payment_statuses": payment_statuses,
        "lead_sources": lead_sources,
        "deadline_statuses": (
            deadline_statuses
        ),
    }
