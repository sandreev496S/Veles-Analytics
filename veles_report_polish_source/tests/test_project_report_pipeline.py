from pathlib import Path
from types import SimpleNamespace

from services.crm.models import CRMProject


def _project(
    tmp_path: Path,
) -> CRMProject:
    folder = (
        tmp_path
        / "VA-2026-001__Client__RXRX"
    )

    (
        folder
        / "03_Client_Uploads"
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    (
        folder
        / "10_Final_Deliverables"
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    source = (
        folder
        / "03_Client_Uploads"
        / "Investor_Deck.pdf"
    )

    source.write_bytes(
        b"test"
    )

    return CRMProject(
        project_id="VA-2026-001",
        client_name="Test Client",
        company_name=(
            "Recursion Pharmaceuticals"
        ),
        ticker="RXRX",
        industry="Biotechnology",
        package="Basic",
        primary_objective=(
            "Investment research"
        ),
        intended_audience=(
            "Private investor"
        ),
        requested_focus_areas=(
            "Revenue growth; liquidity"
        ),
        requested_deliverables=(
            "Basic PDF research brief"
        ),
        folder_path=str(folder),
    )


def test_build_project_report_config(
    tmp_path,
):
    from services.reports.project import (
        build_project_report_config,
    )

    project = _project(tmp_path)

    config = (
        build_project_report_config(
            project
        )
    )

    assert config.project_id == (
        "VA-2026-001"
    )
    assert config.ticker == "RXRX"
    assert config.package == "Basic"
    assert config.client_name == (
        "Test Client"
    )
    assert config.source_documents
    assert (
        config.source_documents[0]
        .filename
        == "Investor_Deck.pdf"
    )


def test_report_naming_and_versioning(
    tmp_path,
):
    from services.reports.project import (
        build_project_report_config,
        build_report_output_path,
        next_report_version,
    )

    config = (
        build_project_report_config(
            _project(tmp_path)
        )
    )

    first = build_report_output_path(
        config
    )

    assert first.name == (
        "RXRX_Basic_Report_v1.pdf"
    )

    first.write_bytes(b"pdf")

    assert next_report_version(
        config
    ) == 2

    second = build_report_output_path(
        config
    )

    assert second.name == (
        "RXRX_Basic_Report_v2.pdf"
    )


def test_project_report_pipeline_applies_context(
    tmp_path,
    monkeypatch,
):
    import services.reports.project.pipeline as pipeline

    project = _project(tmp_path)

    fake_report = SimpleNamespace(
        metadata={},
    )

    monkeypatch.setattr(
        pipeline,
        "assemble_equity_report",
        lambda ticker, profile=None: fake_report,
    )

    report = (
        pipeline
        .assemble_report_for_project(
            project
        )
    )

    assert report.project_id == (
        project.project_id
    )
    assert report.client_name == (
        project.client_name
    )
    assert report.package == "Basic"
    assert (
        report.project_objective
        == "Investment research"
    )
    assert (
        report.metadata[
            "project_context"
        ]["ticker"]
        == "RXRX"
    )
    assert report.report_profile["name"] == "basic"
    assert (
        report.metadata["report_profile"]["include_valuation"]
        is False
    )


def test_current_project_pipeline_requires_ticker(
    tmp_path,
):
    import pytest

    from services.reports.project import (
        assemble_project_report,
        build_project_report_config,
    )

    project = _project(tmp_path)
    project.ticker = ""

    config = (
        build_project_report_config(
            project
        )
    )

    with pytest.raises(
        ValueError,
        match="ticker",
    ):
        assemble_project_report(
            config
        )
