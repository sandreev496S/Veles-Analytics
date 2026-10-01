from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Iterator


@dataclass
class MetricCard:
    label: str
    value: str
    note: str = ""


@dataclass
class ReportSection:
    heading: str
    body: str


@dataclass
class ReportDocument:
    company_name: str
    ticker: str
    industry: str
    date: str
    prepared_by: str = "Veles Analytics"

    toc_items: list[str] = field(default_factory=list)
    snapshot: dict[str, Any] = field(default_factory=dict)

    dashboard_metrics: list[MetricCard] = field(default_factory=list)
    dashboard_business: dict[str, str] = field(default_factory=dict)
    dashboard_investment: dict[str, str] = field(default_factory=dict)

    report_brand: dict[str, Any] = field(default_factory=dict)
    report_profile: dict[str, Any] = field(default_factory=dict)
    executive_summary: dict[str, Any] = field(default_factory=dict)
    analyst_commentary: dict[str, Any] = field(default_factory=dict)
    valuation: dict[str, Any] = field(default_factory=dict)
    financial_render_model: dict[str, Any] = field(default_factory=dict)

    charts: dict[str, str] = field(default_factory=dict)

    thesis_points: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)

    show_competitors: bool = False
    competitors: list[list[Any]] = field(default_factory=list)

    financial_table: list[list[Any]] = field(default_factory=list)
    income_statement: list[list[Any]] = field(default_factory=list)
    balance_sheet: list[list[Any]] = field(default_factory=list)
    cash_flow: list[list[Any]] = field(default_factory=list)
    financial_commentary: list[str] = field(default_factory=list)

    market_snapshot: list[list[Any]] = field(default_factory=list)
    valuation_multiples: list[list[Any]] = field(default_factory=list)
    market_commentary: list[str] = field(default_factory=list)

    sec_filings_table: list[list[Any]] = field(default_factory=list)
    sec_commentary: list[str] = field(default_factory=list)

    sections: list[ReportSection] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    # Temporary compatibility with existing code that treats reports as dictionaries.
    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def keys(self) -> Iterator[str]:
        return iter(self.to_dict().keys())
