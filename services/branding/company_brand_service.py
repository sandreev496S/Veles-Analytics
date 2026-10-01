from __future__ import annotations

from pathlib import Path
from typing import Any


VELES_LOGO_CANDIDATES = [
    Path("assets/veles_logo.png"),
    Path("assets/veles-logo.png"),
    Path("assets/logo.png"),
    Path("static/veles_logo.png"),
    Path("static/logo.png"),
]


VELES_BRAND: dict[str, Any] = {
    "primary": "#0F172A",
    "secondary": "#1D4ED8",
    "accent": "#60A5FA",
    "positive": "#15803D",
    "negative": "#B91C1C",
    "warning": "#D97706",
    "neutral": "#64748B",
    "light_background": "#F8FAFC",
    "card_background": "#F1F5F9",
    "border": "#CBD5E1",
    "logo_path": None,
    "source": "Veles Analytics brand system",
}


def _find_veles_logo() -> str | None:
    for path in VELES_LOGO_CANDIDATES:
        if path.exists():
            return str(path)

    return None


def get_company_brand(
    ticker: str,
    website: str = "",
) -> dict[str, Any]:
    """
    Return the fixed Veles Analytics visual identity.

    The ticker and website arguments remain for backward compatibility,
    but reports no longer inherit company-specific colors.
    """
    brand = dict(VELES_BRAND)
    brand["logo_path"] = _find_veles_logo()
    brand["subject_ticker"] = ticker.upper().strip()
    return brand
