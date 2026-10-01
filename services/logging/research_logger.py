import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

LOG_DIR = Path("reports/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)


def write_research_log(ticker: str, metadata: Dict[str, Any]) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_ticker = ticker.upper().replace("/", "_")
    path = LOG_DIR / f"{safe_ticker}_{timestamp}_research_log.json"

    payload = {
        "ticker": ticker.upper(),
        "logged_at": datetime.now().isoformat(timespec="seconds"),
        "metadata": metadata,
    }

    path.write_text(json.dumps(payload, indent=2, default=str))
    return str(path)
