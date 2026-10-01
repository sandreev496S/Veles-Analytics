from __future__ import annotations

from reportlab.lib.units import inch
from reportlab.platypus import PageBreak, Paragraph, Spacer

from services.pdf.continued_tables import ContinuedLongTable
from services.pdf.sections import section_header_bar
from services.pdf.theme import PDFTheme, VELES_PDF_THEME


def build_professional_appendix(
    report: dict,
    styles: dict,
    *,
    theme: PDFTheme = VELES_PDF_THEME,
) -> list:
    elements: list = [PageBreak()]

    elements.append(
        section_header_bar(
            "Appendix",
            styles,
            subtitle="Supporting financial, regulatory, and market data",
            anchor="appendix",
            theme=theme,
        )
    )

    appendix_sections = [
        {
            "title": "Appendix A — Income Statement",
            "data": report.get("income_statement", []),
            "widths": [
                1.75 * inch,
                1.68 * inch,
                1.68 * inch,
                1.68 * inch,
            ],
        },
        {
            "title": "Appendix B — Balance Sheet",
            "data": report.get("balance_sheet", []),
            "widths": [
                2.4 * inch,
                4.4 * inch,
            ],
        },
        {
            "title": "Appendix C — Cash Flow Statement",
            "data": report.get("cash_flow", []),
            "widths": [
                2.4 * inch,
                4.4 * inch,
            ],
        },
        {
            "title": "Appendix D — SEC Filing Register",
            "data": report.get("sec_filings_table", []),
            "widths": [
                0.9 * inch,
                1.2 * inch,
                1.2 * inch,
                3.5 * inch,
            ],
        },
        {
            "title": "Appendix E — Market Data",
            "data": report.get("market_snapshot", []),
            "widths": [
                2.3 * inch,
                4.5 * inch,
            ],
        },
        {
            "title": "Appendix F — Valuation Multiples",
            "data": report.get("valuation_multiples", []),
            "widths": [
                2.3 * inch,
                4.5 * inch,
            ],
        },
    ]

    for index, section in enumerate(appendix_sections):
        data = section["data"]

        if not data:
            continue

        if index > 0:
            elements.append(PageBreak())

        elements.append(
            ContinuedLongTable(
                section["title"],
                data,
                col_widths=section["widths"],
                theme=theme,
            )
        )

        elements.append(Spacer(1, 0.18 * inch))

    elements.append(PageBreak())

    elements.append(
        section_header_bar(
            "Financial Methodology",
            styles,
            subtitle=(
                "Valuation framework, financial calculations, "
                "and model presentation conventions"
            ),
            anchor="financial_methodology",
            theme=theme,
        )
    )

    financial_methodology_items = [
        (
            "Market capitalization, enterprise value, balance-sheet "
            "values, and reported financial statements are obtained "
            "from configured financial-data providers."
        ),
        (
            "Free cash flow is calculated using normalized operating "
            "cash flow and capital-expenditure data where available."
        ),
        (
            "The driver-based biotechnology DCF separately forecasts "
            "collaboration revenue, product revenue, milestone revenue, "
            "R&D expense, SG&A expense, and other operating expenses."
        ),
        (
            "Terminal value is calculated using the perpetual-growth "
            "method after the explicit forecast period."
        ),
        (
            "Negative enterprise, equity, and per-share scenario values "
            "are preserved in saved model data but displayed using a "
            "$0.00 professional presentation floor."
        ),
        (
            "Bull, base, and bear scenarios are validated to ensure "
            "Bull ≥ Base ≥ Bear."
        ),
    ]

    for item in financial_methodology_items:
        elements.append(
            Paragraph(
                f"• {item}",
                styles["body"],
            )
        )

    elements.append(PageBreak())

    elements.append(
        section_header_bar(
            "Research Methodology and Data Sources",
            styles,
            subtitle=(
                "Data provenance, regulatory sources, "
                "and research limitations"
            ),
            anchor="research_methodology",
            theme=theme,
        )
    )

    research_methodology_items = [
        (
            "Company profile, market data, and reported financial "
            "statements are retrieved through configured providers."
        ),
        (
            "SEC filing metadata is retrieved directly from the "
            "SEC EDGAR submissions API."
        ),
        (
            "Charts are generated from normalized financial and "
            "market data."
        ),
        (
            "Cash runway is estimated using cash and equivalents "
            "divided by the absolute value of annual free-cash-flow burn."
        ),
        (
            "The report distinguishes observed inputs, derived values, "
            "and analyst-provided assumptions."
        ),
        (
            "The report does not independently audit provider data."
        ),
        (
            "ClinicalTrials.gov, FDA, scientific-publication, patent, "
            "and competitive-intelligence sources will be incorporated "
            "through evidence-grounded research providers."
        ),
    ]

    for item in research_methodology_items:
        elements.append(
            Paragraph(
                f"• {item}",
                styles["body"],
            )
        )

    return elements
