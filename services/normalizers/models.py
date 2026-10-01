from typing import Any, Dict, List, TypedDict


class NormalizedCompany(TypedDict):
    company_name: str
    ticker: str
    exchange: str
    sector: str
    industry: str
    website: str
    headquarters: str
    description: str
    business_model: str


class NormalizedMarket(TypedDict):
    currency: str
    as_of: str
    provider: str
    metrics: Dict[str, Any]
    raw_metrics: Dict[str, Any]
    tables: Dict[str, List[List[Any]]]


class NormalizedFinancials(TypedDict):
    currency: str
    period: str
    provider: str
    raw_metrics: Dict[str, Any]
    income_statement: List[List[Any]]
    balance_sheet: List[List[Any]]
    cash_flow: List[List[Any]]
    commentary: List[str]


class NormalizedSEC(TypedDict):
    filings: Dict[str, Any]
    company_facts: Dict[str, Any]


class NormalizedResearchDataset(TypedDict):
    ticker: str
    company: NormalizedCompany
    market: NormalizedMarket
    financials: NormalizedFinancials
    sec: NormalizedSEC
    metadata: Dict[str, Any]
