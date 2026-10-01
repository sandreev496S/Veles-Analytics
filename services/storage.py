import json
from pathlib import Path
from datetime import datetime

SAVE_DIR = Path("saved_valuations")
SAVE_DIR.mkdir(exist_ok=True)


def save_valuation(kind, name, payload):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.lower().replace(" ", "_").replace("/", "_")
    filename = f"{timestamp}_{kind}_{safe_name}.json"
    path = SAVE_DIR / filename

    record = {
        "kind": kind,
        "name": name,
        "created_at": datetime.now().isoformat(),
        "payload": payload,
    }

    with open(path, "w") as f:
        json.dump(record, f, indent=2, default=str)

    return str(path)


def list_valuations():
    records = []

    for path in sorted(SAVE_DIR.glob("*.json"), reverse=True):
        try:
            with open(path, "r") as f:
                data = json.load(f)

            records.append({
                "file": path.name,
                "kind": data.get("kind"),
                "name": data.get("name"),
                "created_at": data.get("created_at"),
            })
        except Exception:
            continue

    return records


def load_valuation(filename):
    path = SAVE_DIR / filename

    with open(path, "r") as f:
        return json.load(f)


def delete_valuation(filename):
    path = SAVE_DIR / filename

    if path.exists() and path.suffix == ".json":
        path.unlink()
        return True

    return False
