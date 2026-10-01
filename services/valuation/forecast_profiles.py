from __future__ import annotations

from dataclasses import replace

from services.valuation.assumption_builder import ForecastProfile


def biotech_platform_profile() -> ForecastProfile:
    """
    Illustrative five-year platform-biotech profile.

    This is not a valuation conclusion and must be reviewed by an analyst.
    """
    return ForecastProfile(
        revenue_growth_rates=[
            0.20,
            0.25,
            0.30,
            0.28,
            0.22,
        ],
        ebit_margins=[
            -5.50,
            -3.50,
            -2.00,
            -0.75,
            0.05,
        ],
        tax_rate=0.21,
        depreciation_amortization_pct_revenue=0.06,
        capex_pct_revenue=0.08,
        nwc_pct_revenue_change=0.05,
        terminal_growth_rate=0.025,
        source="Illustrative Veles platform-biotech profile",
        note=(
            "Requires analyst review. Early-stage biotechnology "
            "forecasts are highly sensitive to partnerships, milestones, "
            "clinical progress, and financing."
        ),
    )


def early_stage_biotech_profile() -> ForecastProfile:
    return ForecastProfile(
        revenue_growth_rates=[
            0.10,
            0.15,
            0.20,
            0.25,
            0.30,
        ],
        ebit_margins=[
            -7.00,
            -5.00,
            -3.00,
            -1.50,
            -0.25,
        ],
        tax_rate=0.21,
        depreciation_amortization_pct_revenue=0.05,
        capex_pct_revenue=0.07,
        nwc_pct_revenue_change=0.04,
        terminal_growth_rate=0.02,
        source="Illustrative Veles early-stage-biotech profile",
        note=(
            "Requires analyst review. A conventional terminal-value DCF "
            "may be inappropriate when terminal-year free cash flow remains negative."
        ),
    )


def mature_growth_profile() -> ForecastProfile:
    return ForecastProfile(
        revenue_growth_rates=[
            0.15,
            0.13,
            0.11,
            0.09,
            0.07,
        ],
        ebit_margins=[
            0.12,
            0.15,
            0.18,
            0.20,
            0.22,
        ],
        tax_rate=0.21,
        depreciation_amortization_pct_revenue=0.04,
        capex_pct_revenue=0.05,
        nwc_pct_revenue_change=0.06,
        terminal_growth_rate=0.025,
        source="Illustrative Veles mature-growth profile",
        note="Requires analyst review.",
    )


def with_overrides(
    profile: ForecastProfile,
    **kwargs,
) -> ForecastProfile:
    return replace(profile, **kwargs)
