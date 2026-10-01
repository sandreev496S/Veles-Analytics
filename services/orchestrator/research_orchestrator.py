from datetime import datetime
from typing import Any

from config.settings import settings
from services.cache.json_cache import get_cache, set_cache
from services.orchestrator.models import ResearchDataset
from services.orchestrator.tasks import DEFAULT_TASKS, get_tasks
from services.providers.registry import get_provider_for_capability
from services.logging.research_logger import write_research_log
from services.normalizers.research_normalizer import normalize_research_dataset
from services.data_quality.validated_attachment import (
    attach_validated_metrics,
)


def build_research_dataset(
    ticker: str,
    use_cache: bool = True,
    selected_capabilities: list[str] | None = None,
) -> ResearchDataset:
    ticker = ticker.upper().strip()
    capabilities = selected_capabilities or DEFAULT_TASKS
    cache_key = f"research_dataset_{ticker}_{'_'.join(capabilities)}"

    if use_cache:
        cached = get_cache(
            cache_key,
            ttl_seconds=settings.cache_ttl_seconds,
        )

        if cached:
            cached["metadata"]["cache_status"] = (
                "loaded_from_cache"
            )

            if "validated_metrics" not in cached:
                attach_validated_metrics(cached)

            return cached

    dataset: dict[str, Any] = {
        "ticker": ticker,
        "company": {},
        "financials": {},
        "market": {},
        "filings": {},
        "company_facts": {},
        "news": {},
        "clinical": {},
        "competitors": {},
        "valuation": {},
        "charts": {},
    }

    errors: dict[str, str] = {}
    task_log: list[dict[str, str]] = []

    for task in get_tasks(capabilities):
        try:
            preferred_provider = None

            if task.capability == "company":
                preferred_provider = settings.company_provider
            elif task.capability == "financials":
                preferred_provider = settings.financial_provider
            elif task.capability == "market":
                preferred_provider = settings.market_provider

            provider = get_provider_for_capability(
                task.capability,
                preferred_provider=preferred_provider,
            )

            method = getattr(provider, task.method_name)
            dataset[task.dataset_key] = method(ticker)

            task_log.append({
                "task": task.name,
                "capability": task.capability,
                "provider": provider.name,
                "status": "success",
            })

        except Exception as e:
            dataset[task.dataset_key] = {}
            errors[task.capability] = str(e)
            task_log.append({
                "task": task.name,
                "capability": task.capability,
                "provider": "none",
                "status": "failed",
            })

    dataset["metadata"] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source": "Veles Research Orchestrator v2",
        "cache_status": "fresh_api_pull",
        "requested_capabilities": capabilities,
        "task_log": task_log,
        "errors": errors,
    }

    normalized_dataset = normalize_research_dataset(dataset)

    try:
        log_path = write_research_log(ticker, normalized_dataset["metadata"])
        normalized_dataset["metadata"]["log_path"] = log_path
    except Exception as e:
        normalized_dataset["metadata"]["log_error"] = str(e)

    attach_validated_metrics(normalized_dataset)

    if use_cache:
        set_cache(cache_key, normalized_dataset)

    return normalized_dataset
