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
            package="Standard",
        )
    )


def test_sec_upload_completes_checklist_items(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist import (
        get_checklist_item,
    )
    from services.crm.checklist_automation import (
        record_project_event,
    )

    project = _create_project(
        tmp_path,
        monkeypatch,
    )

    record_project_event(
        project,
        "sec_filing_uploaded",
    )

    assert get_checklist_item(
        project,
        "required_documents",
    )["completed"]

    assert get_checklist_item(
        project,
        "sec_filings",
    )["completed"]


def test_financial_pull_updates_checklist(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist import (
        get_checklist_item,
    )
    from services.crm.checklist_automation import (
        record_project_event,
    )

    project = _create_project(
        tmp_path,
        monkeypatch,
    )

    record_project_event(
        project,
        "financial_data_pulled",
    )

    assert get_checklist_item(
        project,
        "financial_statements",
    )["completed"]

    assert get_checklist_item(
        project,
        "market_data",
    )["completed"]


def test_research_notes_update_checklist(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist import (
        get_checklist_item,
    )
    from services.crm.checklist_automation import (
        record_project_event,
    )

    project = _create_project(
        tmp_path,
        monkeypatch,
    )

    record_project_event(
        project,
        "research_notes_saved",
    )

    assert get_checklist_item(
        project,
        "research_notes",
    )["completed"]


def test_deliverable_updates_checklist(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist import (
        get_checklist_item,
    )
    from services.crm.checklist_automation import (
        record_project_event,
    )

    project = _create_project(
        tmp_path,
        monkeypatch,
    )

    record_project_event(
        project,
        "deliverable_uploaded",
    )

    assert get_checklist_item(
        project,
        "deliverables_uploaded",
    )["completed"]


def test_repeated_event_does_not_recomplete_item(
    tmp_path,
    monkeypatch,
):
    from services.crm.checklist_automation import (
        record_project_event,
    )
    from services.crm.workspace import (
        list_timeline_events,
    )

    project = _create_project(
        tmp_path,
        monkeypatch,
    )

    first = record_project_event(
        project,
        "research_notes_saved",
    )

    second = record_project_event(
        project,
        "research_notes_saved",
    )

    assert (
        first["metadata"][
            "checklist_items_completed"
        ]
        == ["research_notes"]
    )

    assert (
        second["metadata"][
            "checklist_items_completed"
        ]
        == []
    )

    events = list_timeline_events(
        project
    )

    assert len(
        [
            event
            for event in events
            if event["event_type"]
            == "research_notes_saved"
        ]
    ) == 2
