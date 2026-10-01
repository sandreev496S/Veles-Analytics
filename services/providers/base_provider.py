from abc import ABC
from typing import Any, Dict, Set


class BaseProvider(ABC):
    name: str = "base"
    capabilities: Set[str] = set()

    def supports(self, capability: str) -> bool:
        return capability in self.capabilities

    def health_check(self) -> Dict[str, Any]:
        return {"provider": self.name, "status": "unknown"}

    def get_company_data(self, ticker: str) -> Dict[str, Any]:
        raise NotImplementedError

    def get_financial_data(self, ticker: str) -> Dict[str, Any]:
        raise NotImplementedError

    def get_market_data(self, ticker: str) -> Dict[str, Any]:
        raise NotImplementedError

    def get_filings(self, ticker: str) -> Dict[str, Any]:
        raise NotImplementedError

    def get_company_facts(self, ticker: str) -> Dict[str, Any]:
        raise NotImplementedError

    def get_news(self, ticker: str) -> Dict[str, Any]:
        raise NotImplementedError

    def get_clinical_trials(self, ticker: str) -> Dict[str, Any]:
        raise NotImplementedError
