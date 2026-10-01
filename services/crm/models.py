from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date
from typing import Any


@dataclass
class CRMProject:
    project_id: str
    client_name: str
    company_name: str

    ticker: str = ""
    industry: str = ""
    country: str = ""

    client_email: str = ""
    client_phone: str = ""
    company_website: str = ""

    lead_source: str = "Fiverr"
    package: str = "Basic"
    project_type: str = "Equity Research"
    status: str = "Lead"
    priority: str = "Medium"

    order_date: str = field(
        default_factory=lambda: date.today().isoformat()
    )
    due_date: str = ""
    delivery_date: str = ""

    price_usd: float = 0.0
    hours_worked: float = 0.0
    revision_count: int = 0
    client_rating: float | None = None

    primary_objective: str = ""
    intended_audience: str = ""
    requested_deliverables: str = ""
    requested_focus_areas: str = ""

    assigned_analyst: str = ""
    payment_status: str = "Pending"
    invoice_number: str = ""
    follow_up_date: str = ""
    repeat_client: bool = False

    data_source_mode: str = "Not selected"
    sec_data_status: str = "Not started"
    financial_data_status: str = "Not started"

    folder_path: str = ""
    notes: str = ""

    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def effective_hourly_rate(self) -> float | None:
        if self.hours_worked <= 0:
            return None

        return self.price_usd / self.hours_worked
