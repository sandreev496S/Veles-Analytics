"""Runtime feature flags for local, demo, and deployed environments."""
from __future__ import annotations

import os


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


APP_MODE = os.getenv("APP_MODE", "demo").strip().lower()
DEMO_MODE = APP_MODE == "demo" or _truthy(os.getenv("VELES_DEMO_MODE"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

AUTH_CONFIGURED = bool(SUPABASE_URL and SUPABASE_ANON_KEY)
DATABASE_CONFIGURED = bool(DATABASE_URL)
REPORT_STORAGE_CONFIGURED = bool(
    SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY and DATABASE_URL
)
