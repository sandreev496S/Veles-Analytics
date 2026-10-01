import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from services.providers.registry import list_providers, get_provider_for_capability


def main() -> None:
    print("Registered providers:")
    for provider in list_providers():
        print(provider)

    print("\nCapability routing:")
    for capability in ["company", "financials", "market", "filings", "company_facts"]:
        try:
            provider = get_provider_for_capability(capability)
            print(f"{capability} -> {provider.name}")
        except Exception as e:
            print(f"{capability} -> ERROR: {e}")


if __name__ == "__main__":
    main()
