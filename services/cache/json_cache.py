import json
import time
from pathlib import Path

CACHE_DIR = Path("reports/cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_path(key: str) -> Path:
    safe_key = key.replace("/", "_").replace(":", "_").upper()
    return CACHE_DIR / f"{safe_key}.json"


def get_cache(key: str, ttl_seconds: int = 3600):
    path = _cache_path(key)

    if not path.exists():
        return None

    try:
        payload = json.loads(path.read_text())
        created_at = payload.get("created_at", 0)

        if time.time() - created_at > ttl_seconds:
            return None

        return payload.get("data")
    except Exception:
        return None


def set_cache(key: str, data):
    path = _cache_path(key)

    payload = {
        "created_at": time.time(),
        "data": data,
    }

    path.write_text(json.dumps(payload, indent=2, default=str))
