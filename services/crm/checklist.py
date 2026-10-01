from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from services.crm.models import CRMProject


CHECKLIST_VERSION = 1


BASE_CHECKLIST_ITEMS: list[dict[str, Any]] = [
    {
        "id": "client_objective",
        "category": "Client",
        "title": "Client objective confirmed",
        "required": True,
        "automatic": False,
    },
    {
        "id": "package_verified",
        "category": "Client",
        "title": "Package and project scope verified",
        "required": True,
        "automatic": False,
    },
    {
        "id": "deadline_confirmed",
        "category": "Client",
        "title": "Deadline confirmed",
        "required": True,
        "automatic": False,
    },
    {
        "id": "payment_received",
        "category": "Client",
        "title": "Payment received or confirmed",
        "required": True,
        "automatic": False,
    },
    {
        "id": "required_documents",
        "category": "Data Collection",
        "title": "Required client documents received",
        "required": True,
        "automatic": False,
    },
    {
        "id": "sec_filings",
        "category": "Data Collection",
        "title": "SEC filings imported or reviewed",
        "required": False,
        "automatic": True,
    },
    {
        "id": "financial_statements",
        "category": "Data Collection",
        "title": "Financial statements imported and verified",
        "required": True,
        "automatic": True,
    },
    {
        "id": "market_data",
        "category": "Data Collection",
        "title": "Market data reviewed",
        "required": False,
        "automatic": False,
    },
    {
        "id": "research_notes",
        "category": "Research",
        "title": "Research notes completed",
        "required": True,
        "automatic": True,
    },
    {
        "id": "competitor_analysis",
        "category": "Research",
        "title": "Competitive analysis completed",
        "required": False,
        "automatic": False,
    },
    {
        "id": "investment_thesis",
        "category": "Research",
        "title": "Investment thesis and key risks reviewed",
        "required": True,
        "automatic": False,
    },
    {
        "id": "financial_charts",
        "category": "Quality Control",
        "title": "Financial charts reviewed",
        "required": False,
        "automatic": False,
    },
    {
        "id": "valuation_reviewed",
        "category": "Quality Control",
        "title": "Valuation reviewed, if applicable",
        "required": False,
        "automatic": False,
    },
    {
        "id": "report_proofread",
        "category": "Quality Control",
        "title": "Final report proofread",
        "required": True,
        "automatic": False,
    },
    {
        "id": "deliverables_uploaded",
        "category": "Delivery",
        "title": "Final deliverables uploaded",
        "required": True,
        "automatic": True,
    },
    {
        "id": "client_notified",
        "category": "Delivery",
        "title": "Client notified of delivery",
        "required": True,
        "automatic": False,
    },
]


PACKAGE_OPTIONAL_ITEMS: dict[str, list[dict[str, Any]]] = {
    "Basic": [],
    "Standard": [
        {
            "id": "scenario_analysis",
            "category": "Quality Control",
            "title": "Scenario analysis reviewed",
            "required": False,
            "automatic": False,
        },
        {
            "id": "sensitivity_analysis",
            "category": "Quality Control",
            "title": "Sensitivity analysis reviewed",
            "required": False,
            "automatic": False,
        },
    ],
    "Premium": [
        {
            "id": "scenario_analysis",
            "category": "Quality Control",
            "title": "Scenario analysis reviewed",
            "required": True,
            "automatic": False,
        },
        {
            "id": "sensitivity_analysis",
            "category": "Quality Control",
            "title": "Sensitivity analysis reviewed",
            "required": True,
            "automatic": False,
        },
        {
            "id": "methodology_reviewed",
            "category": "Quality Control",
            "title": "Methodology documentation reviewed",
            "required": True,
            "automatic": False,
        },
        {
            "id": "consultation_completed",
            "category": "Delivery",
            "title": "Client consultation completed, if included",
            "required": False,
            "automatic": False,
        },
    ],
    "Custom": [],
}


class ChecklistCompletionError(ValueError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def checklist_path(project: CRMProject) -> Path:
    if not project.folder_path:
        raise ValueError(
            "Project folder has not been created."
        )

    path = (
        Path(project.folder_path)
        / "00_Project_Dashboard"
        / "checklist.json"
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    return path


def build_default_checklist(
    project: CRMProject,
) -> dict[str, Any]:
    items = deepcopy(BASE_CHECKLIST_ITEMS)

    package_items = PACKAGE_OPTIONAL_ITEMS.get(
        project.package,
        [],
    )

    items.extend(deepcopy(package_items))

    normalized_items = []

    for item in items:
        normalized_items.append({
            **item,
            "completed": False,
            "completed_at": "",
            "updated_at": _utc_now(),
        })

    return {
        "version": CHECKLIST_VERSION,
        "project_id": project.project_id,
        "package": project.package,
        "created_at": _utc_now(),
        "updated_at": _utc_now(),
        "items": normalized_items,
    }


def save_checklist(
    project: CRMProject,
    checklist: dict[str, Any],
) -> Path:
    path = checklist_path(project)

    checklist["updated_at"] = _utc_now()

    temporary = path.with_suffix(
        ".json.tmp"
    )

    temporary.write_text(
        json.dumps(
            checklist,
            indent=2,
        ),
        encoding="utf-8",
    )

    temporary.replace(path)

    return path


def load_checklist(
    project: CRMProject,
    *,
    create_if_missing: bool = True,
) -> dict[str, Any]:
    path = checklist_path(project)

    if not path.exists():
        if not create_if_missing:
            return {}

        checklist = build_default_checklist(
            project
        )

        save_checklist(
            project,
            checklist,
        )

        return checklist

    try:
        checklist = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )
    except (json.JSONDecodeError, OSError):
        if not create_if_missing:
            return {}

        checklist = build_default_checklist(
            project
        )

        save_checklist(
            project,
            checklist,
        )

        return checklist

    checklist.setdefault(
        "version",
        CHECKLIST_VERSION,
    )
    checklist.setdefault(
        "project_id",
        project.project_id,
    )
    checklist.setdefault(
        "package",
        project.package,
    )
    checklist.setdefault(
        "items",
        [],
    )

    return checklist


def get_checklist_item(
    project: CRMProject,
    item_id: str,
) -> dict[str, Any] | None:
    checklist = load_checklist(project)

    return next(
        (
            item
            for item in checklist["items"]
            if item.get("id") == item_id
        ),
        None,
    )


def set_checklist_item(
    project: CRMProject,
    *,
    item_id: str,
    completed: bool,
) -> dict[str, Any]:
    checklist = load_checklist(project)

    selected_item = None

    for item in checklist["items"]:
        if item.get("id") != item_id:
            continue

        item["completed"] = completed
        item["completed_at"] = (
            _utc_now()
            if completed
            else ""
        )
        item["updated_at"] = _utc_now()

        selected_item = item
        break

    if selected_item is None:
        raise KeyError(
            f"Checklist item not found: {item_id}"
        )

    save_checklist(
        project,
        checklist,
    )

    return selected_item


def complete_checklist_item(
    project: CRMProject,
    item_id: str,
) -> dict[str, Any]:
    return set_checklist_item(
        project,
        item_id=item_id,
        completed=True,
    )


def reopen_checklist_item(
    project: CRMProject,
    item_id: str,
) -> dict[str, Any]:
    return set_checklist_item(
        project,
        item_id=item_id,
        completed=False,
    )


def checklist_summary(
    project: CRMProject,
) -> dict[str, Any]:
    checklist = load_checklist(project)
    items = checklist.get("items", [])

    required_items = [
        item
        for item in items
        if item.get("required")
    ]

    completed_required = [
        item
        for item in required_items
        if item.get("completed")
    ]

    completed_total = [
        item
        for item in items
        if item.get("completed")
    ]

    required_total = len(required_items)
    completed_required_count = len(
        completed_required
    )

    progress = (
        completed_required_count
        / required_total
        if required_total
        else 1.0
    )

    incomplete_required = [
        item
        for item in required_items
        if not item.get("completed")
    ]

    return {
        "total_items": len(items),
        "completed_items": len(completed_total),
        "required_items": required_total,
        "completed_required_items": (
            completed_required_count
        ),
        "incomplete_required_items": (
            incomplete_required
        ),
        "progress": progress,
        "progress_percent": round(
            progress * 100,
        ),
        "can_complete_project": (
            len(incomplete_required) == 0
        ),
    }


def validate_project_completion(
    project: CRMProject,
) -> None:
    summary = checklist_summary(project)

    if summary["can_complete_project"]:
        return

    remaining = [
        item.get("title", item.get("id"))
        for item
        in summary["incomplete_required_items"]
    ]

    raise ChecklistCompletionError(
        "Project cannot be marked Completed. "
        "Remaining required checklist items: "
        + "; ".join(remaining)
    )


def reset_checklist(
    project: CRMProject,
) -> dict[str, Any]:
    checklist = build_default_checklist(
        project
    )

    save_checklist(
        project,
        checklist,
    )

    return checklist
