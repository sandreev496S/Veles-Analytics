from __future__ import annotations

import re
from pathlib import Path

from services.reports.project.context import ProjectReportConfig


def _slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value.strip())
    return cleaned.strip("_") or "Report"


def report_name_prefix(
    config: ProjectReportConfig,
    report_type: str = "Basic_Report",
) -> str:
    company = config.ticker or config.company_name or config.project_id
    return f"{_slug(company)}_{_slug(report_type)}"


def list_report_versions(
    config: ProjectReportConfig,
    report_type: str = "Basic_Report",
    extension: str = ".pdf",
):
    if not config.deliverables_folder:
        return []

    folder = Path(config.deliverables_folder)
    if not folder.exists():
        return []

    prefix = report_name_prefix(config, report_type)

    files = sorted(
        folder.glob(f"{prefix}_v*{extension}")
    )

    return files


def next_report_version(
    config: ProjectReportConfig,
    report_type: str = "Basic_Report",
    extension: str = ".pdf",
):
    versions = list_report_versions(
        config,
        report_type,
        extension,
    )

    if not versions:
        return 1

    highest = 0

    pattern = re.compile(r"_v(\d+)")

    for file in versions:
        match = pattern.search(file.stem)
        if match:
            highest = max(highest, int(match.group(1)))

    return highest + 1


def build_report_output_path(
    config: ProjectReportConfig,
    report_type: str = "Basic_Report",
    extension: str = ".pdf",
):
    folder = Path(config.deliverables_folder)
    folder.mkdir(parents=True, exist_ok=True)

    version = next_report_version(
        config,
        report_type,
        extension,
    )

    filename = (
        f"{report_name_prefix(config, report_type)}"
        f"_v{version}{extension}"
    )

    return folder / filename
