from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ReportProfile:
    name: str
    display_name: str
    include_ai_commentary: bool = True
    include_valuation: bool = True
    include_dcf: bool = True
    include_comps: bool = True
    include_scenarios: bool = True
    include_sensitivity: bool = True
    include_price_target: bool = True
    include_rating: bool = True
    include_methodology: bool = True
    include_appendix: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


BASIC_REPORT_PROFILE = ReportProfile(
    name="basic",
    display_name="Basic Company Research Report",
    include_ai_commentary=True,
    include_valuation=False,
    include_dcf=False,
    include_comps=False,
    include_scenarios=False,
    include_sensitivity=False,
    include_price_target=False,
    include_rating=False,
    include_methodology=False,
    include_appendix=False,
)

PROFESSIONAL_REPORT_PROFILE = ReportProfile(
    name="professional",
    display_name="Professional Equity Research Report",
)

_PROFILE_ALIASES = {
    "basic": BASIC_REPORT_PROFILE,
    "starter": BASIC_REPORT_PROFILE,
    "standard": PROFESSIONAL_REPORT_PROFILE,
    "professional": PROFESSIONAL_REPORT_PROFILE,
    "premium": PROFESSIONAL_REPORT_PROFILE,
    "institutional": PROFESSIONAL_REPORT_PROFILE,
}


def resolve_report_profile(package: str | None) -> ReportProfile:
    normalized = str(package or "").strip().lower()
    if not normalized:
        return PROFESSIONAL_REPORT_PROFILE
    return _PROFILE_ALIASES.get(normalized, PROFESSIONAL_REPORT_PROFILE)
