from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO

from services.crm.models import CRMProject


DOCUMENT_DESTINATIONS = {
    "Client Upload": "03_Client_Uploads",
    "SEC Filing": "04_SEC_Data",
    "Financial Statement": "05_Financial_Data",
    "Research Document": "06_Research_Notes",
}


def _safe_filename(filename: str) -> str:
    return Path(filename).name.replace(" ", "_")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def save_project_upload(
    *,
    project: CRMProject,
    filename: str,
    data: bytes,
    document_type: str,
    source_note: str = "",
) -> Path:
    if not project.folder_path:
        raise ValueError(
            "Project folder has not been created."
        )

    destination_name = DOCUMENT_DESTINATIONS.get(
        document_type,
        "03_Client_Uploads",
    )

    destination = (
        Path(project.folder_path)
        / destination_name
    )
    destination.mkdir(parents=True, exist_ok=True)

    safe_name = _safe_filename(filename)
    file_path = destination / safe_name
    file_path.write_bytes(data)

    metadata_path = destination / "document_register.json"

    if metadata_path.exists():
        register = json.loads(
            metadata_path.read_text(
                encoding="utf-8"
            )
        )
    else:
        register = []

    register.append({
        "filename": safe_name,
        "document_type": document_type,
        "source_note": source_note,
        "uploaded_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "size_bytes": len(data),
        "sha256": _sha256(data),
        "path": str(file_path),
    })

    metadata_path.write_text(
        json.dumps(register, indent=2),
        encoding="utf-8",
    )

    return file_path


def list_project_documents(
    project: CRMProject,
) -> list[dict]:
    if not project.folder_path:
        return []

    documents: list[dict] = []

    for destination in DOCUMENT_DESTINATIONS.values():
        register_path = (
            Path(project.folder_path)
            / destination
            / "document_register.json"
        )

        if not register_path.exists():
            continue

        documents.extend(
            json.loads(
                register_path.read_text(
                    encoding="utf-8"
                )
            )
        )

    return documents
