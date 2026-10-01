import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from services.providers.registry import provider_health_report


def main() -> None:
    for row in provider_health_report():
        print(row)


if __name__ == "__main__":
    main()
