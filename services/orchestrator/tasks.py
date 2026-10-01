from dataclasses import dataclass
from typing import Callable, Any


@dataclass(frozen=True)
class ResearchTask:
    name: str
    capability: str
    dataset_key: str
    method_name: str


RESEARCH_TASKS = [
    ResearchTask(
        name="Company Data",
        capability="company",
        dataset_key="company",
        method_name="get_company_data",
    ),
    ResearchTask(
        name="Financial Data",
        capability="financials",
        dataset_key="financials",
        method_name="get_financial_data",
    ),
    ResearchTask(
        name="Market Data",
        capability="market",
        dataset_key="market",
        method_name="get_market_data",
    ),
    ResearchTask(
        name="SEC Filings",
        capability="filings",
        dataset_key="filings",
        method_name="get_filings",
    ),
    ResearchTask(
        name="SEC Company Facts",
        capability="company_facts",
        dataset_key="company_facts",
        method_name="get_company_facts",
    ),
]


DEFAULT_TASKS = [
    "company",
    "financials",
    "market",
]


FULL_RESEARCH_TASKS = [
    "company",
    "financials",
    "market",
    "filings",
    "company_facts",
]


def get_tasks(selected_capabilities: list[str] | None = None) -> list[ResearchTask]:
    selected = selected_capabilities or DEFAULT_TASKS
    return [task for task in RESEARCH_TASKS if task.capability in selected]
