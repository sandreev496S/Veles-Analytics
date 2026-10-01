from services.crm.models import CRMProject


def _create_project(
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

    return storage.create_project(
        CRMProject(
            project_id="VA-2026-001",
            client_name="Test Client",
            company_name="Test Biotech",
            ticker="TEST",
            package="Basic",
        )
    )


def test_project_health_starts_at_risk(
    tmp_path,
    monkeypatch,
):
    from ui.project_workspace import (
        _project_health,
    )

    project = _create_project(
        tmp_path,
        monkeypatch,
    )

    result = _project_health(project)

    assert result["label"] == "At Risk"


def test_project_health_becomes_healthy(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist import (
        complete_checklist_item,
        load_checklist,
    )
    from ui.project_workspace import (
        _project_health,
    )

    project = _create_project(
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

    result = _project_health(project)

    assert result["label"] == "Healthy"
