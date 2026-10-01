from __future__ import annotations

from typing import Any

from services.crm.models import CRMProject
from services.reports.equity_report_assembler import (
    assemble_equity_report,
)
from services.reports.profiles import resolve_report_profile
from services.reports.project.context import (
    ProjectReportConfig,
    build_project_report_config,
)


def _apply_project_context(
    report: Any,
    config: ProjectReportConfig,
) -> Any:
    """
    Attach CRM project context and the resolved rendering
    profile to the assembled report.
    """
    context_payload = config.to_dict()

    profile = resolve_report_profile(
        config.package
    )
    profile_payload = profile.to_dict()

    assignments = {
        "project_id": config.project_id,
        "client_name": config.client_name,
        "package": config.package,
        "project_objective": (
            config.primary_objective
        ),
        "intended_audience": (
            config.intended_audience
        ),
        "requested_focus_areas": (
            config.requested_focus_areas
        ),
        "project_context": context_payload,
        "report_profile": profile_payload,
    }

    for attribute, value in assignments.items():
        try:
            setattr(
                report,
                attribute,
                value,
            )
        except Exception:
            continue

    metadata = getattr(
        report,
        "metadata",
        None,
    )

    if not isinstance(metadata, dict):
        metadata = {}

        try:
            setattr(
                report,
                "metadata",
                metadata,
            )
        except Exception:
            return report

    metadata["project_context"] = context_payload
    metadata["report_profile"] = profile_payload

    return report

def assemble_project_report(
    config: ProjectReportConfig,
) -> Any:
    if not config.ticker:
        raise ValueError(
            "A ticker is required for the current "
            "public-company report pipeline."
        )

    profile = resolve_report_profile(
        config.package
    )

    report = assemble_equity_report(
        config.ticker,
        profile=profile,
    )

    return _apply_project_context(
        report,
        config,
    )


def assemble_report_for_project(
    project: CRMProject,
) -> Any:
    config = build_project_report_config(
        project
    )

    return assemble_project_report(
        config
    )
