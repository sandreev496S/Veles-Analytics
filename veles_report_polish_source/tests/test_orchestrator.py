from services.orchestrator.research_orchestrator import build_research_dataset


def test_orchestrator_returns_dataset():
    research = build_research_dataset("RXRX", use_cache=False)

    assert research["ticker"] == "RXRX"
    assert "company" in research
    assert "financials" in research
    assert "market" in research
    assert "metadata" in research


def test_orchestrator_handles_unknown_ticker():
    research = build_research_dataset("UNKNOWNFAKE123", use_cache=False)

    assert research["ticker"] == "UNKNOWNFAKE123"
    assert "metadata" in research
    assert "errors" in research["metadata"]
