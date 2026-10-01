from __future__ import annotations

from typing import Any

from services.crm.models import CRMProject
from services.reports.equity_report_assembler import (
    assemble_equity_report,
)
from services.reports.profiles import (
    resolve_report_profile,
)
from services.reports.reconciliation import validate_report_for_delivery
from services.reports.project import (
    ProjectReportConfig,
    assemble_project_report,
    assemble_report_for_project,
)


def _delivery_ready(report: Any) -> Any:
    """Fail closed when structured report outputs contradict canonical metrics."""
    findings = validate_report_for_delivery(report, raise_on_error=True)
    metadata = getattr(report, "metadata", None)
    if isinstance(metadata, dict):
        metadata["reconciliation_status"] = "passed"
        metadata["reconciliation_findings"] = [item.to_dict() for item in findings]
    return report


def assemble_report(
    source: (
        str
        | CRMProject
        | ProjectReportConfig
    ),
    *,
    package: str | None = None,
) -> Any:
    if isinstance(
        source,
        ProjectReportConfig,
    ):
        return _delivery_ready(assemble_project_report(
            source
        ))

    if isinstance(
        source,
        CRMProject,
    ):
        return _delivery_ready(assemble_report_for_project(
            source
        ))

    if isinstance(source, str):
        profile = resolve_report_profile(
            package
        )

        return _delivery_ready(assemble_equity_report(
            source,
            profile=profile,
        ))

    raise TypeError(
        "Report source must be a ticker, "
        "CRMProject, or ProjectReportConfig."
    )
