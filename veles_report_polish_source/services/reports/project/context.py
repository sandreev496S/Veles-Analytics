from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from services.crm.models import CRMProject
from services.crm.workspace import list_workspace_files


@dataclass(frozen=True)
class ProjectSourceDocument:
    category: str
    filename: str
    path: str
    size_bytes: int = 0
    modified_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProjectReportConfig:
    project_id: str
    client_name: str
    company_name: str
    ticker: str
    package: str

    industry: str = ""
    country: str = ""
    company_website: str = ""

    primary_objective: str = ""
    intended_audience: str = ""
    requested_deliverables: str = ""
    requested_focus_areas: str = ""

    order_date: str = ""
    due_date: str = ""
    assigned_analyst: str = ""

    project_folder: str = ""
    deliverables_folder: str = ""

    source_documents: tuple[
        ProjectSourceDocument,
        ...
    ] = field(default_factory=tuple)

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["source_documents"] = [
            document.to_dict()
            for document in self.source_documents
        ]
        return payload


def _deliverables_folder(
    project: CRMProject,
) -> str:
    if not project.folder_path:
        return ""

    folder = (
        Path(project.folder_path)
        / "10_Final_Deliverables"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    return str(folder)


def build_project_report_config(
    project: CRMProject,
) -> ProjectReportConfig:
    documents = []

    for row in list_workspace_files(project):
        documents.append(
            ProjectSourceDocument(
                category=str(
                    row.get(
                        "category",
                        "Project File",
                    )
                ),
                filename=str(
                    row.get(
                        "filename",
                        "",
                    )
                ),
                path=str(
                    row.get(
                        "path",
                        "",
                    )
                ),
                size_bytes=int(
                    row.get(
                        "size_bytes",
                        0,
                    )
                    or 0
                ),
                modified_at=str(
                    row.get(
                        "modified_at",
                        "",
                    )
                ),
            )
        )

    return ProjectReportConfig(
        project_id=project.project_id,
        client_name=project.client_name,
        company_name=project.company_name,
        ticker=project.ticker.upper().strip(),
        package=project.package,
        industry=project.industry,
        country=project.country,
        company_website=(
            project.company_website
        ),
        primary_objective=(
            project.primary_objective
        ),
        intended_audience=(
            project.intended_audience
        ),
        requested_deliverables=(
            project.requested_deliverables
        ),
        requested_focus_areas=(
            project.requested_focus_areas
        ),
        order_date=project.order_date,
        due_date=project.due_date,
        assigned_analyst=(
            project.assigned_analyst
        ),
        project_folder=(
            project.folder_path
        ),
        deliverables_folder=(
            _deliverables_folder(project)
        ),
        source_documents=tuple(
            documents
        ),
        metadata={
            "lead_source": (
                project.lead_source
            ),
            "project_type": (
                project.project_type
            ),
            "priority": (
                project.priority
            ),
            "payment_status": (
                project.payment_status
            ),
            "data_source_mode": (
                project.data_source_mode
            ),
            "sec_data_status": (
                project.sec_data_status
            ),
            "financial_data_status": (
                project.financial_data_status
            ),
        },
    )
