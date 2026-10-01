import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from services.orchestrator.research_orchestrator import build_research_dataset


def main() -> None:
    ticker = "RXRX"

    research = build_research_dataset(
        ticker,
        use_cache=False,
        selected_capabilities=["company", "financials", "market", "filings", "company_facts"],
    )

    print("Ticker:", research["ticker"])
    print("Company:", research["company"].get("company_name"))
    print("Market metrics:", list(research["market"].get("metrics", {}).keys())[:5])
    print("Income rows:", len(research["financials"].get("income_statement", [])))
    print("SEC filings status:", research["sec"]["filings"].get("status"))
    print("Recent SEC filings:", len(research["sec"]["filings"].get("recent", [])))
    print("Normalized:", research["metadata"].get("normalized"))
    print("Normalizer:", research["metadata"].get("normalizer"))
    print("Errors:", research["metadata"].get("errors"))


if __name__ == "__main__":
    main()
