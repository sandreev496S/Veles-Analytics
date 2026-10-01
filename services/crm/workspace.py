from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

from services.crm.models import CRMProject


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_json(
    path: Path,
    default: Any,
) -> Any:
    if not path.exists():
        return default

    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except (json.JSONDecodeError, OSError):
        return default


def _write_json(
    path: Path,
    value: Any,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary = path.with_suffix(
        path.suffix + ".tmp"
    )

    temporary.write_text(
        json.dumps(
            value,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    temporary.replace(path)


def _project_root(
    project: CRMProject,
) -> Path:
    if not project.folder_path:
        raise ValueError(
            "The project does not have a folder path."
        )

    root = Path(project.folder_path)
    root.mkdir(
        parents=True,
        exist_ok=True,
    )

    return root


def timeline_path(
    project: CRMProject,
) -> Path:
    return (
        _project_root(project)
        / "00_Project_Dashboard"
        / "timeline.json"
    )


def tasks_path(
    project: CRMProject,
) -> Path:
    return (
        _project_root(project)
        / "00_Project_Dashboard"
        / "tasks.json"
    )


def notes_path(
    project: CRMProject,
) -> Path:
    return (
        _project_root(project)
        / "06_Research_Notes"
        / "research_notes.json"
    )


def add_timeline_event(
    project: CRMProject,
    *,
    event_type: str,
    title: str,
    description: str = "",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    path = timeline_path(project)
    events = _read_json(path, [])

    event = {
        "event_id": str(uuid4()),
        "timestamp": _utc_now(),
        "event_type": event_type,
        "title": title,
        "description": description,
        "metadata": metadata or {},
    }

    events.append(event)
    _write_json(path, events)

    return event


def list_timeline_events(
    project: CRMProject,
) -> list[dict[str, Any]]:
    events = _read_json(
        timeline_path(project),
        [],
    )

    return sorted(
        events,
        key=lambda item: item.get(
            "timestamp",
            "",
        ),
        reverse=True,
    )


def add_task(
    project: CRMProject,
    *,
    title: str,
    description: str = "",
    priority: str = "Medium",
    due_date: str = "",
) -> dict[str, Any]:
    path = tasks_path(project)
    tasks = _read_json(path, [])

    task = {
        "task_id": str(uuid4()),
        "title": title.strip(),
        "description": description.strip(),
        "priority": priority,
        "due_date": due_date,
        "status": "Open",
        "created_at": _utc_now(),
        "completed_at": "",
    }

    tasks.append(task)
    _write_json(path, tasks)

    add_timeline_event(
        project,
        event_type="task_created",
        title=f"Task created: {task['title']}",
        metadata={
            "task_id": task["task_id"],
        },
    )

    return task


def list_tasks(
    project: CRMProject,
) -> list[dict[str, Any]]:
    return _read_json(
        tasks_path(project),
        [],
    )


def update_task_status(
    project: CRMProject,
    *,
    task_id: str,
    status: str,
) -> dict[str, Any]:
    path = tasks_path(project)
    tasks = _read_json(path, [])

    selected = None

    for task in tasks:
        if task.get("task_id") != task_id:
            continue

        task["status"] = status

        if status == "Completed":
            task["completed_at"] = _utc_now()
        else:
            task["completed_at"] = ""

        selected = task
        break

    if selected is None:
        raise KeyError(
            f"Task not found: {task_id}"
        )

    _write_json(path, tasks)

    add_timeline_event(
        project,
        event_type="task_updated",
        title=(
            f"Task marked {status.lower()}: "
            f"{selected['title']}"
        ),
        metadata={
            "task_id": task_id,
            "status": status,
        },
    )

    return selected


def delete_task(
    project: CRMProject,
    task_id: str,
) -> bool:
    path = tasks_path(project)
    tasks = _read_json(path, [])

    selected = next(
        (
            task
            for task in tasks
            if task.get("task_id") == task_id
        ),
        None,
    )

    remaining = [
        task
        for task in tasks
        if task.get("task_id") != task_id
    ]

    if len(remaining) == len(tasks):
        return False

    _write_json(path, remaining)

    add_timeline_event(
        project,
        event_type="task_deleted",
        title=(
            "Task deleted"
            + (
                f": {selected.get('title')}"
                if selected
                else ""
            )
        ),
    )

    return True


def save_research_notes(
    project: CRMProject,
    notes: dict[str, str],
) -> None:
    payload = {
        "updated_at": _utc_now(),
        "sections": notes,
    }

    _write_json(
        notes_path(project),
        payload,
    )

    populated_sections = [
        section
        for section, content in notes.items()
        if str(content).strip()
    ]

    add_timeline_event(
        project,
        event_type="research_notes_saved",
        title="Research notes saved",
        description=(
            "Project research notes were updated."
        ),
        metadata={
            "sections": populated_sections,
            "section_count": len(
                populated_sections
            ),
        },
    )


def load_research_notes(
    project: CRMProject,
) -> dict[str, str]:
    payload = _read_json(
        notes_path(project),
        {},
    )

    sections = payload.get(
        "sections",
        {},
    )

    if not isinstance(sections, dict):
        return {}

    return {
        str(key): str(value)
        for key, value in sections.items()
    }


def list_workspace_files(
    project: CRMProject,
) -> list[dict[str, Any]]:
    root = _project_root(project)

    groups = {
        "Client Uploads": "03_Client_Uploads",
        "SEC Data": "04_SEC_Data",
        "Financial Data": "05_Financial_Data",
        "Research Notes": "06_Research_Notes",
        "Charts": "08_Charts",
        "Drafts": "09_Drafts",
        "Final Deliverables": (
            "10_Final_Deliverables"
        ),
    }

    rows: list[dict[str, Any]] = []

    for category, folder_name in groups.items():
        folder = root / folder_name

        if not folder.exists():
            continue

        for file_path in folder.rglob("*"):
            if not file_path.is_file():
                continue

            rows.append({
                "category": category,
                "filename": file_path.name,
                "path": str(file_path),
                "size_bytes": file_path.stat().st_size,
                "modified_at": datetime.fromtimestamp(
                    file_path.stat().st_mtime,
                    tz=timezone.utc,
                ).isoformat(),
            })

    return sorted(
        rows,
        key=lambda item: item["modified_at"],
        reverse=True,
    )


def save_deliverable(
    project: CRMProject,
    *,
    filename: str,
    data: bytes,
    description: str = "",
) -> Path:
    destination = (
        _project_root(project)
        / "10_Final_Deliverables"
    )

    destination.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_filename = Path(
        filename
    ).name.replace(" ", "_")

    output = destination / safe_filename
    output.write_bytes(data)

    metadata_path = (
        destination
        / "deliverables_register.json"
    )

    register = _read_json(
        metadata_path,
        [],
    )

    register.append({
        "filename": safe_filename,
        "description": description,
        "path": str(output),
        "size_bytes": len(data),
        "uploaded_at": _utc_now(),
    })

    _write_json(
        metadata_path,
        register,
    )

    from services.crm.checklist_automation import (
        record_project_event,
    )

    record_project_event(
        project,
        "deliverable_uploaded",
        description=(
            description
            or f"Deliverable added: {safe_filename}"
        ),
        metadata={
            "filename": safe_filename,
            "path": str(output),
            "size_bytes": len(data),
        },
    )

    return output


def delete_workspace_file(
    project: CRMProject,
    file_path: str,
) -> bool:
    root = _project_root(project).resolve()
    target = Path(file_path).resolve()

    if root not in target.parents:
        raise ValueError(
            "The file is outside the project workspace."
        )

    if not target.exists() or not target.is_file():
        return False

    target.unlink()

    add_timeline_event(
        project,
        event_type="file_deleted",
        title=f"File deleted: {target.name}",
    )

    return True
