from services.reports.profiles import (
    BASIC_REPORT_PROFILE,
    PROFESSIONAL_REPORT_PROFILE,
    resolve_report_profile,
)


def test_basic_profile_excludes_valuation_features():
    profile = resolve_report_profile("Basic")

    assert profile is BASIC_REPORT_PROFILE
    assert profile.include_valuation is False
    assert profile.include_dcf is False
    assert profile.include_comps is False
    assert profile.include_price_target is False
    assert profile.include_rating is False


def test_professional_profile_preserves_full_report():
    profile = resolve_report_profile("Professional")

    assert profile is PROFESSIONAL_REPORT_PROFILE
    assert profile.include_valuation is True
    assert profile.include_dcf is True
    assert profile.include_comps is True


def test_unknown_package_defaults_to_professional():
    assert (
        resolve_report_profile("Custom")
        is PROFESSIONAL_REPORT_PROFILE
    )
