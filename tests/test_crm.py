from pathlib import Path

from services.crm.models import CRMProject
from services.crm.storage import (
    create_project,
    load_projects,
)
from services.crm.excel_export import (
    export_master_crm,
)


def test_create_project(
    tmp_path,
    monkeypatch,
):
    import services.crm.storage as storage
    import services.crm.excel_export as excel_export

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
    monkeypatch.setattr(
        excel_export,
        "EXPORT_ROOT",
        tmp_path / "exports",
    )

    project = CRMProject(
        project_id="VA-2026-001",
        client_name="Test Client",
        company_name="Recursion Pharmaceuticals",
        ticker="RXRX",
        package="Standard",
    )

    created = create_project(project)

    assert created.folder_path
    assert Path(created.folder_path).exists()
    assert len(load_projects()) == 1

    workbook = export_master_crm(
        tmp_path / "crm.xlsx"
    )

    assert workbook.exists()
    assert workbook.stat().st_size > 0
