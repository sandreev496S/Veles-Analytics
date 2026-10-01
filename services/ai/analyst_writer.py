from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

try:
    from openai import OpenAI
except ModuleNotFoundError:  # optional when AI commentary is disabled or mocked
    OpenAI = None

from config.settings import settings
from services.ai.evidence_builder import build_ai_evidence_packet
from services.ai.models import AnalystCommentary


CACHE_ROOT = Path("reports/cache/ai")
CACHE_ROOT.mkdir(parents=True, exist_ok=True)


SYSTEM_INSTRUCTIONS = """
You are the Veles Analytics evidence-grounded equity research writer.

MANDATORY RULES:
1. Use only facts present in the supplied evidence packet.
2. Never use outside knowledge, memory, assumptions, or invented facts.
3. Every factual paragraph must cite one or more evidence_ids copied exactly.
4. Do not cite an evidence_id unless it directly supports the statement.
5. If evidence is absent, conflicting, stale, or insufficient, explicitly say so.
6. Clearly distinguish observation from interpretation.
7. Do not issue a buy, sell, or hold recommendation.
8. Do not claim causality unless the supplied evidence directly establishes it.
9. Do not calculate a metric unless the necessary figures are present.
10. Keep every section concise and suitable for professional equity research.
11. Mention material data limitations in the limitations field.
12. Confidence must be high, medium, or low.
"""


def _cache_path(
    ticker: str,
    evidence_packet: dict[str, Any],
    model: str,
) -> Path:
    serialized = json.dumps(
        {
            "model": model,
            "evidence": evidence_packet,
        },
        sort_keys=True,
        default=str,
    ).encode("utf-8")

    digest = hashlib.sha256(serialized).hexdigest()[:16]
    safe_model = model.replace("/", "_")

    return CACHE_ROOT / f"{ticker.lower()}_{safe_model}_{digest}.json"


def _fallback_commentary(reason: str) -> AnalystCommentary:
    unavailable = {
        "text": (
            "AI analyst commentary was unavailable for this report run. "
            "The underlying live financial, market, and SEC data remain included."
        ),
        "evidence_ids": [],
        "confidence": "low",
    }

    return AnalystCommentary(
        executive_summary=unavailable,
        revenue_analysis=unavailable,
        research_spending_analysis=unavailable,
        liquidity_analysis=unavailable,
        profitability_analysis=unavailable,
        market_valuation_analysis=unavailable,
        sec_filing_analysis=unavailable,
        risk_assessment=unavailable,
        catalyst_assessment=unavailable,
        limitations=[reason],
    )


def generate_analyst_commentary(
    research: dict[str, Any],
    use_cache: bool = True,
) -> AnalystCommentary:
    """
    Generate evidence-grounded commentary.

    This function always returns AnalystCommentary. API failures, parsing
    failures, timeouts, missing keys, and invalid citations return a typed
    fallback instead of stopping report generation.
    """
    if not settings.ai_commentary_enabled:
        return _fallback_commentary(
            "AI commentary is disabled by configuration."
        )

    if OpenAI is None:
        return _fallback_commentary(
            "The optional openai package is not installed."
        )

    if not os.getenv("OPENAI_API_KEY"):
        return _fallback_commentary(
            "OPENAI_API_KEY is not configured."
        )

    try:
        evidence_packet = build_ai_evidence_packet(research)
    except Exception as exc:
        return _fallback_commentary(
            f"Evidence packet construction failed: {exc}"
        )

    ticker = str(research.get("ticker", "unknown"))
    model = settings.openai_model

    cache_path = _cache_path(
        ticker=ticker,
        evidence_packet=evidence_packet,
        model=model,
    )

    if use_cache and cache_path.exists():
        try:
            return AnalystCommentary.model_validate_json(
                cache_path.read_text()
            )
        except Exception:
            # Ignore corrupt or outdated cache and generate a fresh result.
            pass

    prompt = {
        "task": (
            "Produce concise, evidence-grounded analyst commentary using only "
            "the supplied evidence records."
        ),
        "evidence_packet": evidence_packet,
    }

    try:
        client = OpenAI(
            timeout=settings.ai_timeout_seconds,
            max_retries=0,
        )

        response = client.responses.parse(
            model=model,
            input=[
                {
                    "role": "system",
                    "content": SYSTEM_INSTRUCTIONS,
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        prompt,
                        indent=2,
                        default=str,
                    ),
                },
            ],
            text_format=AnalystCommentary,
        )

        commentary = response.output_parsed

        if commentary is None:
            return _fallback_commentary(
                "The AI response contained no parsed commentary."
            )

        valid_ids = {
            record["evidence_id"]
            for record in evidence_packet.get("evidence", [])
        }

        commentary_sections = [
            commentary.executive_summary,
            commentary.revenue_analysis,
            commentary.research_spending_analysis,
            commentary.liquidity_analysis,
            commentary.profitability_analysis,
            commentary.market_valuation_analysis,
            commentary.sec_filing_analysis,
            commentary.risk_assessment,
            commentary.catalyst_assessment,
        ]

        invalid_ids: set[str] = set()

        for section in commentary_sections:
            for evidence_id in section.evidence_ids:
                if evidence_id not in valid_ids:
                    invalid_ids.add(evidence_id)

        if invalid_ids:
            return _fallback_commentary(
                "AI output referenced invalid evidence IDs: "
                + ", ".join(sorted(invalid_ids))
            )

        try:
            cache_path.write_text(
                commentary.model_dump_json(indent=2)
            )
        except Exception:
            # Cache failure must never prevent report generation.
            pass

        return commentary

    except Exception as exc:
        return _fallback_commentary(
            f"AI commentary generation failed: {type(exc).__name__}: {exc}"
        )
