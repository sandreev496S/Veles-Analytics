from pathlib import Path

import pytest

from services.crm.models import CRMProject


def create_test_project(
    tmp_path,
    monkeypatch,
    *,
    package="Standard",
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

    return storage.create_project(
        CRMProject(
            project_id="VA-2026-001",
            client_name="Test Client",
            company_name="Test Biotechnology",
            ticker="TEST",
            package=package,
        )
    )


def test_new_project_creates_checklist(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist import (
        checklist_path,
        load_checklist,
    )

    project = create_test_project(
        tmp_path,
        monkeypatch,
    )

    path = checklist_path(project)

    assert path.exists()

    checklist = load_checklist(project)

    assert checklist["project_id"] == (
        project.project_id
    )
    assert checklist["items"]


def test_checklist_progress_is_derived(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist import (
        checklist_summary,
        complete_checklist_item,
    )

    project = create_test_project(
        tmp_path,
        monkeypatch,
    )

    initial = checklist_summary(project)

    assert initial["progress_percent"] == 0
    assert not initial[
        "can_complete_project"
    ]

    complete_checklist_item(
        project,
        "client_objective",
    )

    updated = checklist_summary(project)

    assert (
        updated["completed_required_items"]
        == 1
    )
    assert updated["progress_percent"] > 0


def test_completed_item_can_be_reopened(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist import (
        complete_checklist_item,
        get_checklist_item,
        reopen_checklist_item,
    )

    project = create_test_project(
        tmp_path,
        monkeypatch,
    )

    complete_checklist_item(
        project,
        "client_objective",
    )

    assert get_checklist_item(
        project,
        "client_objective",
    )["completed"]

    reopen_checklist_item(
        project,
        "client_objective",
    )

    assert not get_checklist_item(
        project,
        "client_objective",
    )["completed"]


def test_incomplete_project_is_rejected(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist import (
        ChecklistCompletionError,
        validate_project_completion,
    )

    project = create_test_project(
        tmp_path,
        monkeypatch,
    )

    with pytest.raises(
        ChecklistCompletionError
    ):
        validate_project_completion(
            project
        )


def test_project_can_complete_when_required_items_done(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist import (
        complete_checklist_item,
        load_checklist,
        validate_project_completion,
    )

    project = create_test_project(
        tmp_path,
        monkeypatch,
    )

    checklist = load_checklist(project)

    for item in checklist["items"]:
        if item["required"]:
            complete_checklist_item(
                project,
                item["id"],
            )

    validate_project_completion(project)


def test_premium_package_adds_required_items(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist import (
        load_checklist,
    )

    project = create_test_project(
        tmp_path,
        monkeypatch,
        package="Premium",
    )

    checklist = load_checklist(project)

    items = {
        item["id"]: item
        for item in checklist["items"]
    }

    assert items[
        "scenario_analysis"
    ]["required"]

    assert items[
        "sensitivity_analysis"
    ]["required"]

    assert items[
        "methodology_reviewed"
    ]["required"]
