from __future__ import annotations

from typing import Any

import pandas as pd

from services.crm.models import CRMProject


SEARCHABLE_FIELDS = [
    "project_id",
    "client_name",
    "company_name",
    "ticker",
    "industry",
    "country",
    "lead_source",
    "package",
    "project_type",
    "status",
    "priority",
    "primary_objective",
    "intended_audience",
    "requested_deliverables",
    "requested_focus_areas",
    "payment_status",
    "notes",
]


def projects_to_dataframe(
    projects: list[CRMProject],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []

    for project in projects:
        row = project.to_dict()
        row["effective_hourly_rate"] = (
            project.effective_hourly_rate
        )
        rows.append(row)

    if not rows:
        return pd.DataFrame()

    return pd.DataFrame(rows)


def build_search_text(
    dataframe: pd.DataFrame,
) -> pd.Series:
    if dataframe.empty:
        return pd.Series(dtype=str)

    existing_fields = [
        field
        for field in SEARCHABLE_FIELDS
        if field in dataframe.columns
    ]

    if not existing_fields:
        return pd.Series(
            [""] * len(dataframe),
            index=dataframe.index,
            dtype=str,
        )

    return (
        dataframe[existing_fields]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .str.lower()
    )


def apply_project_filters(
    dataframe: pd.DataFrame,
    *,
    search_query: str = "",
    statuses: list[str] | None = None,
    packages: list[str] | None = None,
    priorities: list[str] | None = None,
    payment_statuses: list[str] | None = None,
    lead_sources: list[str] | None = None,
    deadline_statuses: list[str] | None = None,
) -> pd.DataFrame:
    if dataframe.empty:
        return dataframe.copy()

    result = dataframe.copy()

    if search_query.strip():
        search_text = build_search_text(result)
        query = search_query.strip().lower()

        result = result[
            search_text.str.contains(
                query,
                regex=False,
                na=False,
            )
        ]

    filters = {
        "status": statuses,
        "package": packages,
        "priority": priorities,
        "payment_status": payment_statuses,
        "lead_source": lead_sources,
        "deadline_status": deadline_statuses,
    }

    for column, selected_values in filters.items():
        if (
            selected_values
            and column in result.columns
        ):
            result = result[
                result[column].isin(
                    selected_values
                )
            ]

    return result.reset_index(drop=True)


def unique_filter_options(
    dataframe: pd.DataFrame,
    column: str,
) -> list[str]:
    if (
        dataframe.empty
        or column not in dataframe.columns
    ):
        return []

    return sorted(
        {
            str(value)
            for value in dataframe[column].dropna()
            if str(value).strip()
        }
    )
