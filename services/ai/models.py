from __future__ import annotations

from pydantic import BaseModel, Field


class EvidenceBackedParagraph(BaseModel):
    text: str = Field(
        description=(
            "Concise analyst commentary based only on supplied evidence. "
            "State insufficient evidence when necessary."
        )
    )
    evidence_ids: list[str] = Field(
        default_factory=list,
        description="IDs copied exactly from the supplied evidence packet.",
    )
    confidence: str = Field(
        description="One of: high, medium, low."
    )


class AnalystCommentary(BaseModel):
    executive_summary: EvidenceBackedParagraph
    revenue_analysis: EvidenceBackedParagraph
    research_spending_analysis: EvidenceBackedParagraph
    liquidity_analysis: EvidenceBackedParagraph
    profitability_analysis: EvidenceBackedParagraph
    market_valuation_analysis: EvidenceBackedParagraph
    sec_filing_analysis: EvidenceBackedParagraph
    risk_assessment: EvidenceBackedParagraph
    catalyst_assessment: EvidenceBackedParagraph

    limitations: list[str] = Field(default_factory=list)
