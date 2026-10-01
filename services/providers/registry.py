from typing import List

from services.providers.base_provider import BaseProvider
from services.providers.yahoo_provider import YahooProvider
from services.providers.sec_provider import SECProvider


PROVIDERS: List[BaseProvider] = [
    YahooProvider(),
    SECProvider(),
]


def get_provider_for_capability(capability: str, preferred_provider: str | None = None) -> BaseProvider:
    if preferred_provider:
        for provider in PROVIDERS:
            if provider.name == preferred_provider and provider.supports(capability):
                return provider

    for provider in PROVIDERS:
        if provider.supports(capability):
            return provider

    raise ValueError(f"No provider registered for capability: {capability}")


def list_providers() -> list[dict]:
    return [
        {
            "name": provider.name,
            "capabilities": sorted(provider.capabilities),
        }
        for provider in PROVIDERS
    ]


def get_company_provider(provider_name: str = "yfinance"):
    return get_provider_for_capability("company", provider_name)


def get_financial_provider(provider_name: str = "yfinance"):
    return get_provider_for_capability("financials", provider_name)


def get_market_provider(provider_name: str = "yfinance"):
    return get_provider_for_capability("market", provider_name)


def provider_health_report() -> list[dict]:
    report = []
    for provider in PROVIDERS:
        try:
            health = provider.health_check()
        except Exception as e:
            health = {
                "provider": provider.name,
                "status": "error",
                "error": str(e),
            }

        report.append({
            "name": provider.name,
            "capabilities": sorted(provider.capabilities),
            "health": health,
        })

    return report
