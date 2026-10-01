from __future__ import annotations

from datetime import date
from typing import Any

import pandas as pd


CLOSED_STATUSES = {
    "Completed",
    "Archived",
}


def deadline_details(
    due_date_value: Any,
    *,
    today: date | pd.Timestamp | None = None,
) -> dict[str, Any]:
    reference_date = (
        pd.Timestamp.today().normalize()
        if today is None
        else pd.Timestamp(today).normalize()
    )

    due_date = pd.to_datetime(
        due_date_value,
        errors="coerce",
    )

    if pd.isna(due_date):
        return {
            "deadline_status": "No Deadline",
            "days_remaining": None,
            "deadline_sort_order": 5,
        }

    due_date = due_date.normalize()
    days_remaining = int(
        (due_date - reference_date).days
    )

    if days_remaining < 0:
        status = "Overdue"
        sort_order = 0
    elif days_remaining == 0:
        status = "Due Today"
        sort_order = 1
    elif days_remaining <= 3:
        status = "Due Soon"
        sort_order = 2
    else:
        status = "On Track"
        sort_order = 3

    return {
        "deadline_status": status,
        "days_remaining": days_remaining,
        "deadline_sort_order": sort_order,
    }


def add_deadline_columns(
    dataframe: pd.DataFrame,
    *,
    today: date | pd.Timestamp | None = None,
) -> pd.DataFrame:
    if dataframe.empty:
        return dataframe.copy()

    result = dataframe.copy()

    if "due_date" not in result.columns:
        result["deadline_status"] = (
            "No Deadline"
        )
        result["days_remaining"] = None
        result["deadline_sort_order"] = 5
        return result

    details = result["due_date"].apply(
        lambda value: deadline_details(
            value,
            today=today,
        )
    )

    result["deadline_status"] = details.apply(
        lambda item: item["deadline_status"]
    )
    result["days_remaining"] = details.apply(
        lambda item: item["days_remaining"]
    )
    result["deadline_sort_order"] = (
        details.apply(
            lambda item: item[
                "deadline_sort_order"
            ]
        )
    )

    return result


def calculate_dashboard_metrics(
    dataframe: pd.DataFrame,
) -> dict[str, Any]:
    if dataframe.empty:
        return {
            "total_projects": 0,
            "active_projects": 0,
            "completed_projects": 0,
            "due_this_week": 0,
            "overdue_projects": 0,
            "paid_revenue": 0.0,
            "outstanding_revenue": 0.0,
        }

    status_series = dataframe.get(
        "status",
        pd.Series(
            [""] * len(dataframe),
            index=dataframe.index,
        ),
    )

    active_mask = ~status_series.isin(
        CLOSED_STATUSES
    )

    deadline_series = dataframe.get(
        "deadline_status",
        pd.Series(
            ["No Deadline"] * len(dataframe),
            index=dataframe.index,
        ),
    )

    payment_series = dataframe.get(
        "payment_status",
        pd.Series(
            [""] * len(dataframe),
            index=dataframe.index,
        ),
    )

    price_series = pd.to_numeric(
        dataframe.get(
            "price_usd",
            pd.Series(
                [0.0] * len(dataframe),
                index=dataframe.index,
            ),
        ),
        errors="coerce",
    ).fillna(0.0)

    due_this_week_mask = (
        active_mask
        & deadline_series.isin(
            [
                "Due Today",
                "Due Soon",
            ]
        )
    )

    overdue_mask = (
        active_mask
        & deadline_series.eq("Overdue")
    )

    paid_mask = payment_series.eq("Paid")

    return {
        "total_projects": len(dataframe),
        "active_projects": int(
            active_mask.sum()
        ),
        "completed_projects": int(
            status_series.eq(
                "Completed"
            ).sum()
        ),
        "due_this_week": int(
            due_this_week_mask.sum()
        ),
        "overdue_projects": int(
            overdue_mask.sum()
        ),
        "paid_revenue": float(
            price_series[paid_mask].sum()
        ),
        "outstanding_revenue": float(
            price_series[
                ~paid_mask
                & ~status_series.eq("Archived")
            ].sum()
        ),
    }


def due_projects(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    if dataframe.empty:
        return dataframe.copy()

    result = dataframe.copy()

    if "status" in result.columns:
        result = result[
            ~result["status"].isin(
                CLOSED_STATUSES
            )
        ]

    if "deadline_status" in result.columns:
        result = result[
            result["deadline_status"].isin(
                [
                    "Overdue",
                    "Due Today",
                    "Due Soon",
                ]
            )
        ]

    sort_columns = [
        column
        for column in [
            "deadline_sort_order",
            "due_date",
            "priority",
        ]
        if column in result.columns
    ]

    if sort_columns:
        result = result.sort_values(
            sort_columns,
            ascending=True,
            na_position="last",
        )

    return result.reset_index(drop=True)
