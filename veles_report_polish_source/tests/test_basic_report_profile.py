from services.reports.equity_report_assembler import assemble_equity_report
from services.reports.profiles import BASIC_REPORT_PROFILE


def test_basic_report_omits_valuation_content():
    report = assemble_equity_report(
        "RXRX",
        profile=BASIC_REPORT_PROFILE,
    )

    assert report.report_profile["name"] == "basic"
    assert report.valuation["status"] == "excluded"
    assert report.valuation_multiples == []
    assert not any(
        "Valuation" in item
        for item in report.toc_items
    )
    assert not any(
        section.heading == "Valuation Discussion"
        for section in report.sections
    )


def test_basic_report_uses_commercial_section_order():
    report = assemble_equity_report(
        "RXRX",
        profile=BASIC_REPORT_PROFILE,
    )

    expected = [
        "Executive Summary",
        "Company Overview",
        "Business Model",
        "Industry Overview",
        "Historical Financial Performance",
        "Revenue Analysis",
        "Cash, Liquidity & Debt",
        "SEC Filing Highlights",
        "Key Risks",
        "Potential Catalysts",
        "Conclusion",
        "Sources",
        "Disclaimer",
    ]

    assert [
        item.split(". ", 1)[1]
        for item in report.toc_items
    ] == expected
