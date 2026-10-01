from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from services.valuation.integration_validation import (
    validate_complete_dcf_payload,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
VALUATION_ROOT = PROJECT_ROOT / "reports" / "valuations"
VALUATION_ROOT.mkdir(parents=True, exist_ok=True)


def _safe_name(value: str) -> str:
    cleaned = re.sub(
        r"[^A-Za-z0-9_.-]+",
        "_",
        value.strip(),
    )
    return cleaned.strip("_") or "valuation"


def save_valuation(
    ticker: str,
    payload: dict[str, Any],
    *,
    name: str = "Base DCF",
) -> str:
    validate_complete_dcf_payload(payload)

    ticker = ticker.upper().strip()
    ticker_dir = VALUATION_ROOT / ticker.lower()
    ticker_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%dT%H%M%SZ")

    filename = (
        f"{timestamp}_{_safe_name(name).lower()}.json"
    )
    output_path = ticker_dir / filename

    saved_payload = {
        "schema_version": "1.1",
        "valuation_engine": "Veles DCF Engine v1",
        "ticker": ticker,
        "name": name,
        "saved_at": now.isoformat(),
        "payload": payload,
    }

    serialized = json.dumps(
        saved_payload,
        indent=2,
        default=str,
    )

    temporary_path = output_path.with_suffix(
        output_path.suffix + ".tmp"
    )

    temporary_path.write_text(serialized)
    temporary_path.replace(output_path)

    return str(output_path)


def list_saved_valuations(
    ticker: str,
) -> list[dict[str, Any]]:
    ticker_dir = VALUATION_ROOT / ticker.lower().strip()

    if not ticker_dir.exists():
        return []

    results: list[dict[str, Any]] = []

    for path in sorted(
        ticker_dir.glob("*.json"),
        reverse=True,
    ):
        try:
            data = json.loads(path.read_text())
        except Exception:
            continue

        results.append({
            "path": str(path),
            "name": data.get("name", path.stem),
            "ticker": data.get(
                "ticker",
                ticker.upper(),
            ),
            "saved_at": data.get("saved_at"),
        })

    return results


def load_valuation(
    path: str,
) -> dict[str, Any]:
    valuation_path = Path(path)

    if not valuation_path.exists():
        raise FileNotFoundError(
            f"Saved valuation not found: {path}"
        )

    data = json.loads(valuation_path.read_text())

    if "payload" not in data:
        raise ValueError(
            "Saved valuation does not contain a payload."
        )

    validate_complete_dcf_payload(
        data["payload"]
    )

    return data


def load_latest_valuation(
    ticker: str,
) -> dict[str, Any] | None:
    saved = list_saved_valuations(ticker)

    if not saved:
        return None

    return load_valuation(saved[0]["path"])
