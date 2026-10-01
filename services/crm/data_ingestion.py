from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from services.crm.models import CRMProject
from services.crm.storage import update_project


def _to_serializable(value: Any) -> Any:
    if hasattr(value, "to_dict"):
        return _to_serializable(value.to_dict())

    if isinstance(value, dict):
        return {
            str(key): _to_serializable(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            _to_serializable(item)
            for item in value
        ]

    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            pass

    return value


def pull_sec_and_financial_data(
    project: CRMProject,
    *,
    pull_sec: bool = True,
    pull_financials: bool = True,
    use_cache: bool = True,
) -> dict[str, Any]:
    if not project.ticker:
        raise ValueError(
            "A ticker is required for automatic data pulls."
        )

    if not project.folder_path:
        raise ValueError(
            "Project folder has not been created."
        )

    capabilities: list[str] = [
        "company",
        "market",
    ]

    if pull_financials:
        capabilities.append("financials")

    if pull_sec:
        capabilities.extend([
            "filings",
            "company_facts",
        ])

    from services.orchestrator.research_orchestrator import (
        build_research_dataset,
    )

    dataset = build_research_dataset(
        project.ticker.upper(),
        use_cache=use_cache,
        selected_capabilities=capabilities,
    )

    serializable = _to_serializable(dataset)

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S")

    written_files: list[str] = []

    if pull_sec:
        sec_path = (
            Path(project.folder_path)
            / "04_SEC_Data"
            / f"{project.ticker.upper()}_sec_{timestamp}.json"
        )

        sec_payload = (
            serializable.get("sec", {})
            if isinstance(serializable, dict)
            else {}
        )

        sec_path.write_text(
            json.dumps(
                sec_payload,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

        written_files.append(str(sec_path))

    if pull_financials:
        financial_path = (
            Path(project.folder_path)
            / "05_Financial_Data"
            / (
                f"{project.ticker.upper()}_"
                f"financials_{timestamp}.json"
            )
        )

        financial_payload = {
            "company": serializable.get(
                "company",
                {},
            ),
            "financials": serializable.get(
                "financials",
                {},
            ),
            "market": serializable.get(
                "market",
                {},
            ),
        }

        financial_path.write_text(
            json.dumps(
                financial_payload,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

        written_files.append(
            str(financial_path)
        )

    updates: dict[str, Any] = {
        "data_source_mode": (
            "Automatic provider pull"
        ),
    }

    if pull_sec:
        updates["sec_data_status"] = "Pulled"

    if pull_financials:
        updates[
            "financial_data_status"
        ] = "Pulled"

    update_project(
        project.project_id,
        updates,
    )

    return {
        "ticker": project.ticker.upper(),
        "capabilities": capabilities,
        "written_files": written_files,
        "dataset": serializable,
    }
