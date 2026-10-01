from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    Image,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from services.pdf.theme import PDFTheme, VELES_PDF_THEME


def build_cover(
    report: dict,
    styles: dict,
    *,
    theme: PDFTheme = VELES_PDF_THEME,
) -> list:
    elements: list = []

    report_brand = report.get("report_brand", {})
    logo_path = report_brand.get("logo_path")

    elements.append(Spacer(1, 0.35 * inch))

    if logo_path and Path(str(logo_path)).exists():
        logo_row = Table(
            [[
                Image(
                    str(logo_path),
                    width=1.15 * inch,
                    height=1.15 * inch,
                    kind="proportional",
                ),
                "",
            ]],
            colWidths=[1.3 * inch, theme.content_width - 1.3 * inch],
        )
        logo_row.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ]
            )
        )
        elements.append(logo_row)

    elements.append(Spacer(1, 0.65 * inch))

    elements.append(
        Paragraph(
            "VELES ANALYTICS",
            styles["eyebrow"],
        )
    )

    elements.append(
        Paragraph(
            "EQUITY RESEARCH",
            styles["cover_report_type"],
        )
    )

    elements.append(
        Paragraph(
            escape(str(report["company_name"])),
            styles["cover_company"],
        )
    )

    ticker = escape(str(report["ticker"]))
    industry = escape(str(report["industry"]))
    report_date = escape(str(report["date"]))

    metadata_table = Table(
        [
            ["Ticker", ticker],
            ["Industry", industry],
            ["Report Date", report_date],
            ["Prepared By", "Veles Analytics"],
        ],
        colWidths=[1.2 * inch, 4.8 * inch],
        hAlign="LEFT",
    )

    metadata_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("TEXTCOLOR", (0, 0), (0, -1), theme.neutral),
                ("TEXTCOLOR", (1, 0), (1, -1), theme.primary),
                ("LINEBELOW", (0, 0), (-1, -1), 0.3, theme.light_border),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elements.extend(
        [
            Spacer(1, 0.28 * inch),
            metadata_table,
            Spacer(1, 1.0 * inch),
        ]
    )

    positioning = Table(
        [[
            Paragraph(
                (
                    "Independent research focused on biotechnology, "
                    "neurotechnology, and frontier-science companies."
                ),
                styles["body"],
            )
        ]],
        colWidths=[theme.content_width],
    )

    positioning.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), theme.card_background),
                ("LINEBEFORE", (0, 0), (0, -1), 5, theme.secondary),
                ("BOX", (0, 0), (-1, -1), 0.4, theme.light_border),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )

    elements.append(positioning)
    elements.append(Spacer(1, 1.15 * inch))

    elements.append(
        Paragraph(
            (
                "For informational purposes only. This document does not "
                "constitute investment advice."
            ),
            styles["small"],
        )
    )

    return elements
