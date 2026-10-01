from datetime import date

import pandas as pd

from services.crm.dashboard import (
    add_deadline_columns,
    calculate_dashboard_metrics,
    deadline_details,
    due_projects,
)
from services.crm.search import (
    apply_project_filters,
)


def test_deadline_statuses():
    today = date(2026, 7, 16)

    assert deadline_details(
        "2026-07-15",
        today=today,
    )["deadline_status"] == "Overdue"

    assert deadline_details(
        "2026-07-16",
        today=today,
    )["deadline_status"] == "Due Today"

    assert deadline_details(
        "2026-07-18",
        today=today,
    )["deadline_status"] == "Due Soon"

    assert deadline_details(
        "2026-07-25",
        today=today,
    )["deadline_status"] == "On Track"

    assert deadline_details(
        "",
        today=today,
    )["deadline_status"] == "No Deadline"


def test_project_search_and_filters():
    dataframe = pd.DataFrame([
        {
            "project_id": "VA-001",
            "client_name": "Johnson Capital",
            "company_name": "Recursion",
            "ticker": "RXRX",
            "status": "In Progress",
            "package": "Standard",
            "priority": "High",
            "payment_status": "Paid",
            "lead_source": "Fiverr",
            "deadline_status": "Due Soon",
            "primary_objective": (
                "Investment research"
            ),
            "notes": "",
        },
        {
            "project_id": "VA-002",
            "client_name": "Apollo",
            "company_name": "CRISPR Therapeutics",
            "ticker": "CRSP",
            "status": "Completed",
            "package": "Premium",
            "priority": "Medium",
            "payment_status": "Pending",
            "lead_source": "Website",
            "deadline_status": "On Track",
            "primary_objective": (
                "Competitive analysis"
            ),
            "notes": "",
        },
    ])

    result = apply_project_filters(
        dataframe,
        search_query="recursion",
        statuses=["In Progress"],
        packages=[],
        priorities=[],
        payment_statuses=[],
        lead_sources=[],
        deadline_statuses=[],
    )

    assert len(result) == 1
    assert result.iloc[0]["ticker"] == "RXRX"


def test_dashboard_metrics():
    dataframe = pd.DataFrame([
        {
            "status": "In Progress",
            "deadline_status": "Due Soon",
            "payment_status": "Paid",
            "price_usd": 225,
        },
        {
            "status": "In Progress",
            "deadline_status": "Overdue",
            "payment_status": "Pending",
            "price_usd": 450,
        },
        {
            "status": "Completed",
            "deadline_status": "On Track",
            "payment_status": "Paid",
            "price_usd": 95,
        },
    ])

    metrics = calculate_dashboard_metrics(
        dataframe
    )

    assert metrics["total_projects"] == 3
    assert metrics["active_projects"] == 2
    assert metrics["completed_projects"] == 1
    assert metrics["due_this_week"] == 1
    assert metrics["overdue_projects"] == 1
    assert metrics["paid_revenue"] == 320
    assert metrics["outstanding_revenue"] == 450


def test_due_projects_excludes_completed():
    dataframe = pd.DataFrame([
        {
            "project_id": "VA-001",
            "status": "In Progress",
            "deadline_status": "Overdue",
            "deadline_sort_order": 0,
            "due_date": "2026-07-15",
        },
        {
            "project_id": "VA-002",
            "status": "Completed",
            "deadline_status": "Overdue",
            "deadline_sort_order": 0,
            "due_date": "2026-07-14",
        },
    ])

    result = due_projects(dataframe)

    assert list(result["project_id"]) == [
        "VA-001"
    ]


def test_add_deadline_columns():
    dataframe = pd.DataFrame([
        {
            "project_id": "VA-001",
            "due_date": "2026-07-16",
        }
    ])

    result = add_deadline_columns(
        dataframe,
        today=date(2026, 7, 16),
    )

    assert (
        result.iloc[0]["deadline_status"]
        == "Due Today"
    )
