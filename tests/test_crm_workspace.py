from pathlib import Path

from services.crm.models import CRMProject


def test_project_workspace_persistence(
    tmp_path,
    monkeypatch,
):
    import services.crm.storage as storage

    monkeypatch.setattr(
        storage,
        "CRM_ROOT",
        tmp_path,
    )
    monkeypatch.setattr(
        storage,
        "PROJECT_ROOT",
        tmp_path / "projects",
    )
    monkeypatch.setattr(
        storage,
        "DATABASE_PATH",
        tmp_path / "projects.json",
    )
    monkeypatch.setattr(
        storage,
        "EXPORT_ROOT",
        tmp_path / "exports",
    )

    project = storage.create_project(
        CRMProject(
            project_id="VA-2026-001",
            client_name="Test Client",
            company_name="Test Biotech",
            ticker="TEST",
            package="Standard",
        )
    )

    from services.crm.workspace import (
        add_task,
        list_tasks,
        list_timeline_events,
        load_research_notes,
        save_research_notes,
        update_task_status,
    )

    task = add_task(
        project,
        title="Review latest filing",
        priority="High",
        due_date="2026-07-20",
    )

    assert len(list_tasks(project)) == 1

    update_task_status(
        project,
        task_id=task["task_id"],
        status="Completed",
    )

    assert (
        list_tasks(project)[0]["status"]
        == "Completed"
    )

    save_research_notes(
        project,
        {
            "Investment Thesis": (
                "Illustrative research note."
            ),
        },
    )

    notes = load_research_notes(project)

    assert (
        notes["Investment Thesis"]
        == "Illustrative research note."
    )

    events = list_timeline_events(project)

    assert len(events) >= 4
    assert Path(project.folder_path).exists()
