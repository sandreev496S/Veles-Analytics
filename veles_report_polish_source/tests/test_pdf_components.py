from reportlab.platypus import Table

from services.pdf.callouts import (
    analyst_callout,
    three_column_callouts,
)
from services.pdf.theme import (
    VELES_PDF_THEME,
    build_pdf_styles,
)


def test_three_column_callouts_fit_content_width():
    styles = build_pdf_styles()

    component = three_column_callouts(
        ("Bull Case", "One\nTwo\nThree", "positive"),
        ("Bear Case", "One\nTwo\nThree", "negative"),
        ("Catalysts", "One\nTwo\nThree", "insight"),
        styles,
    )

    assert isinstance(component, Table)

    total_width = sum(component._argW)

    assert total_width <= VELES_PDF_THEME.content_width + 1


def test_full_width_callout_uses_report_width():
    styles = build_pdf_styles()

    component = analyst_callout(
        "Financial Assessment",
        "Revenue increased while cash burn remained elevated.",
        styles,
        width=VELES_PDF_THEME.content_width,
    )

    assert isinstance(component, Table)
    assert component._argW[0] == VELES_PDF_THEME.content_width


def _executive_summary_report():
    return {
        "executive_summary": {
            "company": (
                "Recursion Pharmaceuticals "
                "(NASDAQ: RXRX)"
            ),
            "industry": (
                "AI-Enabled Drug Discovery"
            ),
            "business_model": (
                "Recursion develops machine-learning "
                "platforms that combine automated "
                "experimentation with large-scale "
                "biological datasets."
            ),
            "investment_highlights": [
                (
                    "Significant cash reserves support "
                    "continued research and development."
                ),
                (
                    "The proprietary platform provides "
                    "differentiated biological data."
                ),
                (
                    "Strategic partnerships expand "
                    "development opportunities."
                ),
            ],
            "key_risks": [
                "Clinical development outcomes remain uncertain.",
                "Commercialization timelines may be lengthy.",
                "Continued losses may require future financing.",
            ],
            "key_catalysts": [
                "Clinical data and pipeline updates.",
                "New strategic partnership announcements.",
                "Quarterly financial results.",
            ],
            "financial_snapshot": {
                "Revenue": "$58M",
                "Cash": "$518M",
                "Debt": "$120M",
                "Net Income": "-$420M",
                "Free Cash Flow": "-$360M",
                "Estimated Runway": "1.4 years",
            },
        }
    }


def test_executive_summary_page_builds():
    from reportlab.platypus import PageBreak

    from services.pdf.executive_summary import (
        build_executive_summary_page,
    )

    styles = build_pdf_styles()

    elements = build_executive_summary_page(
        _executive_summary_report(),
        styles,
    )

    assert elements
    assert isinstance(
        elements[0],
        PageBreak,
    )


def test_executive_summary_can_render_without_page_break():
    from services.pdf.executive_summary import (
        build_executive_summary_page,
    )

    styles = build_pdf_styles()

    elements = build_executive_summary_page(
        _executive_summary_report(),
        styles,
        include_page_break=False,
    )

    assert elements
    assert not any(
        element.__class__.__name__ == "PageBreak"
        for element in elements
    )


def test_executive_summary_component_fits_report_width():
    from services.pdf.executive_summary import (
        _financial_snapshot,
        _identity_block,
        _summary_payload,
    )

    styles = build_pdf_styles()
    report = _executive_summary_report()
    summary = _summary_payload(report)

    identity = _identity_block(
        summary,
        styles,
        theme=VELES_PDF_THEME,
    )

    snapshot = _financial_snapshot(
        summary,
        styles,
        theme=VELES_PDF_THEME,
    )

    assert sum(identity._argW) <= (
        VELES_PDF_THEME.content_width + 1
    )

    assert sum(snapshot._argW) <= (
        VELES_PDF_THEME.content_width + 1
    )


def test_executive_summary_handles_missing_fields():
    from services.pdf.executive_summary import (
        build_executive_summary_page,
    )

    styles = build_pdf_styles()

    elements = build_executive_summary_page(
        {
            "executive_summary": {
                "company": "Example Corp (NASDAQ: EXM)",
            }
        },
        styles,
        include_page_break=False,
    )

    assert elements
