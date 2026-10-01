from typing import Any, Dict, TypedDict


class ResearchMetadata(TypedDict):
    generated_at: str
    source: str
    cache_status: str
    errors: Dict[str, str]


class ResearchDataset(TypedDict):
    ticker: str
    company: Dict[str, Any]
    financials: Dict[str, Any]
    market: Dict[str, Any]
    filings: Dict[str, Any]
    company_facts: Dict[str, Any]
    news: Dict[str, Any]
    clinical: Dict[str, Any]
    competitors: Dict[str, Any]
    valuation: Dict[str, Any]
    charts: Dict[str, Any]
    metadata: Dict[str, Any]
