from services.ai.evidence_builder import build_ai_evidence_packet
from services.orchestrator.research_orchestrator import build_research_dataset


def test_evidence_packet_has_unique_ids():
    research = build_research_dataset(
        "RXRX",
        use_cache=False,
        selected_capabilities=[
            "company",
            "financials",
            "market",
            "filings",
            "company_facts",
        ],
    )

    packet = build_ai_evidence_packet(research)
    ids = [
        item["evidence_id"]
        for item in packet["evidence"]
    ]

    assert ids
    assert len(ids) == len(set(ids))


def test_every_evidence_record_has_source():
    research = build_research_dataset(
        "RXRX",
        use_cache=False,
        selected_capabilities=[
            "company",
            "financials",
            "market",
            "filings",
            "company_facts",
        ],
    )

    packet = build_ai_evidence_packet(research)

    for item in packet["evidence"]:
        assert item["source"]
        assert item["evidence_id"]
