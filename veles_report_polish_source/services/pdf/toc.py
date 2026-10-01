from __future__ import annotations

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer
from reportlab.platypus.tableofcontents import TableOfContents

from services.pdf.theme import PDFTheme, VELES_PDF_THEME


def build_automatic_toc(
    styles: dict,
    *,
    theme: PDFTheme = VELES_PDF_THEME,
) -> list:
    toc = TableOfContents()

    toc.levelStyles = [
        ParagraphStyle(
            "VelesTOCLevel0",
            parent=styles["toc_item"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=15,
            leftIndent=0,
            firstLineIndent=0,
            textColor=theme.primary,
            spaceBefore=5,
            spaceAfter=3,
        ),
        ParagraphStyle(
            "VelesTOCLevel1",
            parent=styles["toc_item"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            leftIndent=18,
            firstLineIndent=0,
            textColor=theme.body_text,
            spaceBefore=2,
            spaceAfter=2,
        ),
    ]

    toc.dotsMinLevel = 0

    return [
        Paragraph(
            "Table of Contents",
            styles["toc_title"],
        ),
        Spacer(1, 0.12 * inch),
        toc,
    ]
