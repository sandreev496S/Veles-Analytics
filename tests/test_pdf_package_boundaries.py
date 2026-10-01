from __future__ import annotations

import ast
from pathlib import Path

from services.reports.profiles import (
    BASIC_REPORT_PROFILE,
    PROFESSIONAL_REPORT_PROFILE,
)


EXPORTER_PATH = Path("services/pdf_report_exporter.py")


def _source() -> str:
    return EXPORTER_PATH.read_text(encoding="utf-8")


def test_phase2_exporter_is_valid_python():
    ast.parse(_source())


def test_basic_profile_excludes_every_premium_pdf_feature():
    profile = BASIC_REPORT_PROFILE.to_dict()

    assert profile["include_valuation"] is False
    assert profile["include_dcf"] is False
    assert profile["include_comps"] is False
    assert profile["include_scenarios"] is False
    assert profile["include_sensitivity"] is False
    assert profile["include_price_target"] is False
    assert profile["include_rating"] is False
    assert profile["include_methodology"] is False
    assert profile["include_appendix"] is False


def test_professional_profile_keeps_every_premium_pdf_feature():
    profile = PROFESSIONAL_REPORT_PROFILE.to_dict()

    assert profile["include_valuation"] is True
    assert profile["include_dcf"] is True
    assert profile["include_comps"] is True
    assert profile["include_scenarios"] is True
    assert profile["include_sensitivity"] is True
    assert profile["include_price_target"] is True
    assert profile["include_rating"] is True
    assert profile["include_methodology"] is True
    assert profile["include_appendix"] is True


def test_exporter_reads_serialized_report_profile():
    source = _source()

    assert "profile = _report_profile(report)" in source
    assert "_profile_feature_enabled(" in source
    assert "_is_basic_profile(profile)" in source


def test_valuation_renderer_is_feature_gated():
    source = _source()

    valuation_call = source.index(
        "build_valuation_section("
    )
    gate = source.rfind(
        "if include_valuation_section:",
        0,
        valuation_call,
    )

    assert gate != -1


def test_professional_appendix_is_feature_gated():
    source = _source()

    appendix_call = source.index(
        "build_professional_appendix("
    )
    gate = source.rfind(
        "if include_appendix:",
        0,
        appendix_call,
    )

    assert gate != -1


def test_basic_market_section_excludes_valuation_material():
    source = _source()

    assert (
        "if include_valuation\n"
        "            else \"Market Data\""
    ) in source

    assert (
        "include_valuation\n"
        '        and report.get("valuation_multiples")'
    ) in source

    assert (
        "include_valuation\n"
        '        and report.get("market_commentary")'
    ) in source


def test_valuation_ai_commentary_is_feature_gated():
    source = _source()

    assert "if include_valuation:" in source
    assert '"Market Valuation Analysis"' in source


def test_professional_only_narrative_sections_are_filtered():
    source = _source()

    assert "professional_only_headings = {" in source
    assert '"Valuation Discussion"' in source
    assert '"DCF Forecast"' in source
    assert '"Sensitivity Analysis"' in source
    assert '"Valuation Methodology"' in source
    assert '"Professional Appendix"' in source


def test_legacy_reports_default_to_professional_behavior():
    source = _source()

    assert "default: bool = True" in source
