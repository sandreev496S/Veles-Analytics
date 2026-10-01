from __future__ import annotations

import json
import re
from dataclasses import fields
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from services.crm.models import CRMProject


CRM_ROOT = Path("data/crm")
PROJECT_ROOT = CRM_ROOT / "projects"
DATABASE_PATH = CRM_ROOT / "projects.json"
EXPORT_ROOT = CRM_ROOT / "exports"


PROJECT_SUBFOLDERS = [
    "00_Project_Dashboard",
    "01_Client_Communication",
    "02_Order_Details",
    "03_Client_Uploads",
    "04_SEC_Data",
    "05_Financial_Data",
    "06_Research_Notes",
    "07_Competitors",
    "08_Charts",
    "09_Drafts",
    "10_Final_Deliverables",
    "11_Internal_Notes",
]


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _slug(value: str) -> str:
    cleaned = re.sub(
        r"[^A-Za-z0-9]+",
        "_",
        value.strip(),
    )

    return cleaned.strip("_") or "project"


def ensure_crm_directories() -> None:
    CRM_ROOT.mkdir(parents=True, exist_ok=True)
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)

    if not DATABASE_PATH.exists():
        DATABASE_PATH.write_text(
            json.dumps([], indent=2),
            encoding="utf-8",
        )


def load_projects() -> list[CRMProject]:
    ensure_crm_directories()

    raw = json.loads(
        DATABASE_PATH.read_text(encoding="utf-8")
    )

    allowed_fields = {
        item.name
        for item in fields(CRMProject)
    }

    projects: list[CRMProject] = []

    for row in raw:
        clean = {
            key: value
            for key, value in row.items()
            if key in allowed_fields
        }

        projects.append(CRMProject(**clean))

    return projects


def save_projects(
    projects: list[CRMProject],
) -> None:
    ensure_crm_directories()

    DATABASE_PATH.write_text(
        json.dumps(
            [
                project.to_dict()
                for project in projects
            ],
            indent=2,
        ),
        encoding="utf-8",
    )


def build_project_folder(
    project: CRMProject,
) -> Path:
    ensure_crm_directories()

    folder_name = (
        f"{_slug(project.project_id)}__"
        f"{_slug(project.client_name)}__"
        f"{_slug(project.company_name)}"
    )

    project_path = PROJECT_ROOT / folder_name
    project_path.mkdir(parents=True, exist_ok=True)

    for subfolder in PROJECT_SUBFOLDERS:
        (project_path / subfolder).mkdir(
            parents=True,
            exist_ok=True,
        )

    dashboard_path = (
        project_path
        / "00_Project_Dashboard"
        / "project_overview.json"
    )

    dashboard_path.write_text(
        json.dumps(
            project.to_dict(),
            indent=2,
        ),
        encoding="utf-8",
    )

    return project_path


def next_project_id(
    projects: list[CRMProject],
) -> str:
    year = datetime.now().year
    prefix = f"VA-{year}-"

    sequence_numbers: list[int] = []

    for project in projects:
        if not project.project_id.startswith(prefix):
            continue

        try:
            sequence_numbers.append(
                int(project.project_id.split("-")[-1])
            )
        except ValueError:
            continue

    next_number = (
        max(sequence_numbers, default=0) + 1
    )

    return f"{prefix}{next_number:03d}"


def create_project(
    project: CRMProject,
) -> CRMProject:
    projects = load_projects()

    if any(
        existing.project_id == project.project_id
        for existing in projects
    ):
        raise ValueError(
            f"Project ID already exists: "
            f"{project.project_id}"
        )

    now = _utc_now()

    project.created_at = now
    project.updated_at = now

    project_path = build_project_folder(project)
    project.folder_path = str(project_path)

    build_project_folder(project)

    projects.append(project)
    save_projects(projects)

    try:
        from services.crm.checklist import (
            load_checklist,
        )

        load_checklist(
            project,
            create_if_missing=True,
        )
    except Exception:
        pass

    try:
        from services.crm.workspace import (
            add_timeline_event,
        )

        add_timeline_event(
            project,
            event_type="project_created",
            title="Project created",
            description=(
                f"Client: {project.client_name}; "
                f"Company: {project.company_name}; "
                f"Package: {project.package}"
            ),
        )
    except Exception:
        pass

    return project


def update_project(
    project_id: str,
    updates: dict[str, Any],
) -> CRMProject:
    projects = load_projects()

    project = next(
        (
            item
            for item in projects
            if item.project_id == project_id
        ),
        None,
    )

    if project is None:
        raise KeyError(
            f"Project not found: {project_id}"
        )

    editable_fields = {
        item.name
        for item in fields(CRMProject)
    }

    for key, value in updates.items():
        if key in editable_fields:
            setattr(project, key, value)

    project.updated_at = _utc_now()

    build_project_folder(project)
    save_projects(projects)

    return project


def get_project(
    project_id: str,
) -> CRMProject | None:
    return next(
        (
            project
            for project in load_projects()
            if project.project_id == project_id
        ),
        None,
    )


def delete_project(
    project_id: str,
) -> bool:
    projects = load_projects()

    remaining = [
        project
        for project in projects
        if project.project_id != project_id
    ]

    if len(remaining) == len(projects):
        return False

    save_projects(remaining)
    return True
