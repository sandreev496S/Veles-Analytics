from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class DataProviderSettings:
    company_provider: str = os.getenv("VELES_COMPANY_PROVIDER", "yfinance")
    financial_provider: str = os.getenv("VELES_FINANCIAL_PROVIDER", "yfinance")
    market_provider: str = os.getenv("VELES_MARKET_PROVIDER", "yfinance")
    cache_ttl_seconds: int = int(os.getenv("VELES_CACHE_TTL_SECONDS", "3600"))
    openai_model: str = os.getenv("VELES_OPENAI_MODEL", "gpt-5-mini")
    ai_commentary_enabled: bool = (
        os.getenv("VELES_AI_COMMENTARY_ENABLED", "true").lower() == "true"
    )
    ai_timeout_seconds: float = float(
        os.getenv("VELES_AI_TIMEOUT_SECONDS", "25")
    )


settings = DataProviderSettings()
