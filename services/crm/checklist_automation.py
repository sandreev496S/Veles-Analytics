from __future__ import annotations

from typing import Any

from services.crm.checklist import (
    get_checklist_item,
    set_checklist_item,
)
from services.crm.models import CRMProject
from services.crm.workspace import add_timeline_event


EVENT_CHECKLIST_MAPPING: dict[str, list[str]] = {
    "client_document_uploaded": [
        "required_documents",
    ],
    "sec_filing_uploaded": [
        "required_documents",
        "sec_filings",
    ],
    "financial_statement_uploaded": [
        "required_documents",
        "financial_statements",
    ],
    "sec_data_pulled": [
        "sec_filings",
    ],
    "financial_data_pulled": [
        "financial_statements",
        "market_data",
    ],
    "research_notes_saved": [
        "research_notes",
    ],
    "competitor_analysis_saved": [
        "competitor_analysis",
    ],
    "deliverable_uploaded": [
        "deliverables_uploaded",
    ],
    "client_notified": [
        "client_notified",
    ],
    "payment_confirmed": [
        "payment_received",
    ],
}


EVENT_TITLES: dict[str, str] = {
    "client_document_uploaded": (
        "Client document uploaded"
    ),
    "sec_filing_uploaded": (
        "SEC filing uploaded"
    ),
    "financial_statement_uploaded": (
        "Financial statement uploaded"
    ),
    "sec_data_pulled": (
        "SEC data pulled"
    ),
    "financial_data_pulled": (
        "Financial data pulled"
    ),
    "research_notes_saved": (
        "Research notes saved"
    ),
    "competitor_analysis_saved": (
        "Competitive analysis saved"
    ),
    "deliverable_uploaded": (
        "Deliverable uploaded"
    ),
    "client_notified": (
        "Client notified"
    ),
    "payment_confirmed": (
        "Payment confirmed"
    ),
}


def _complete_mapped_item(
    project: CRMProject,
    item_id: str,
) -> bool:
    item = get_checklist_item(
        project,
        item_id,
    )

    if item is None:
        return False

    if item.get("completed"):
        return False

    set_checklist_item(
        project,
        item_id=item_id,
        completed=True,
    )

    return True


def record_project_event(
    project: CRMProject,
    event_type: str,
    *,
    description: str = "",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Record one meaningful CRM workflow event.

    The function:
    1. Completes any checklist items mapped to the event.
    2. Creates one timeline event.
    3. Avoids duplicate checklist-completion activity when
       the mapped checklist item was already complete.
    """
    mapped_items = EVENT_CHECKLIST_MAPPING.get(
        event_type,
        [],
    )

    completed_items: list[str] = []

    for item_id in mapped_items:
        if _complete_mapped_item(
            project,
            item_id,
        ):
            completed_items.append(
                item_id
            )

    event_metadata = dict(
        metadata or {}
    )

    event_metadata[
        "checklist_items_completed"
    ] = completed_items

    title = EVENT_TITLES.get(
        event_type,
        event_type.replace(
            "_",
            " ",
        ).title(),
    )

    if completed_items:
        checklist_text = ", ".join(
            completed_items
        )

        event_description = (
            description.strip()
            + (
                "\n\n"
                if description.strip()
                else ""
            )
            + (
                "Checklist updated: "
                f"{checklist_text}"
            )
        )
    else:
        event_description = (
            description.strip()
        )

    return add_timeline_event(
        project,
        event_type=event_type,
        title=title,
        description=event_description,
        metadata=event_metadata,
    )
