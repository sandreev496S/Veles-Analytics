from __future__ import annotations

from typing import Any

from services.crm.models import CRMProject
from services.reports.equity_report_assembler import (
    assemble_equity_report,
)
from services.reports.project import (
    ProjectReportConfig,
    assemble_project_report,
    assemble_report_for_project,
)


def assemble_report(
    source: (
        str
        | CRMProject
        | ProjectReportConfig
    ),
) -> Any:
    if isinstance(
        source,
        ProjectReportConfig,
    ):
        return assemble_project_report(
            source
        )

    if isinstance(
        source,
        CRMProject,
    ):
        return assemble_report_for_project(
            source
        )

    if isinstance(source, str):
        return assemble_equity_report(
            source
        )

    raise TypeError(
        "Report source must be a ticker, "
        "CRMProject, or ProjectReportConfig."
    )
