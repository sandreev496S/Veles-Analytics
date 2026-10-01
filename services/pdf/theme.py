from __future__ import annotations

from dataclasses import dataclass

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch


@dataclass(frozen=True)
class PDFTheme:
    primary: colors.Color = colors.HexColor("#0F172A")
    secondary: colors.Color = colors.HexColor("#1D4ED8")
    accent: colors.Color = colors.HexColor("#60A5FA")

    positive: colors.Color = colors.HexColor("#15803D")
    negative: colors.Color = colors.HexColor("#B91C1C")
    warning: colors.Color = colors.HexColor("#D97706")

    neutral: colors.Color = colors.HexColor("#64748B")
    muted: colors.Color = colors.HexColor("#94A3B8")
    body_text: colors.Color = colors.HexColor("#1F2937")

    border: colors.Color = colors.HexColor("#CBD5E1")
    light_border: colors.Color = colors.HexColor("#E2E8F0")
    light_background: colors.Color = colors.HexColor("#F8FAFC")
    card_background: colors.Color = colors.HexColor("#F1F5F9")
    white: colors.Color = colors.white

    page_width: float = 8.5 * inch
    page_height: float = 11 * inch

    margin_left: float = 0.65 * inch
    margin_right: float = 0.65 * inch
    margin_top: float = 0.65 * inch
    margin_bottom: float = 0.7 * inch

    content_width: float = 7.2 * inch

    section_gap: float = 0.22 * inch
    subsection_gap: float = 0.12 * inch
    paragraph_gap: float = 0.08 * inch
    table_gap: float = 0.16 * inch
    figure_gap: float = 0.18 * inch


VELES_PDF_THEME = PDFTheme()


def build_pdf_styles(
    theme: PDFTheme = VELES_PDF_THEME,
) -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()

    return {
        "eyebrow": ParagraphStyle(
            "VelesEyebrow",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=10,
            tracking=1.2,
            textColor=theme.secondary,
            spaceAfter=7,
        ),
        "title": ParagraphStyle(
            "VelesTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=31,
            textColor=theme.primary,
            alignment=0,
            spaceAfter=12,
        ),
        "cover_company": ParagraphStyle(
            "VelesCoverCompany",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=28,
            textColor=theme.primary,
            alignment=0,
            spaceAfter=10,
        ),
        "cover_report_type": ParagraphStyle(
            "VelesCoverReportType",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=15,
            textColor=theme.neutral,
            spaceAfter=22,
        ),
        "subtitle": ParagraphStyle(
            "VelesSubtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=theme.neutral,
            spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "VelesH1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=theme.primary,
            spaceBefore=14,
            spaceAfter=9,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "VelesH2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            textColor=theme.secondary,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "VelesH3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=14,
            textColor=theme.primary,
            spaceBefore=8,
            spaceAfter=4,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "VelesBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.8,
            leading=14.2,
            textColor=theme.body_text,
            spaceAfter=7,
        ),
        "body_compact": ParagraphStyle(
            "VelesBodyCompact",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12.5,
            textColor=theme.body_text,
            spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "VelesSmall",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10.5,
            textColor=theme.neutral,
        ),
        "caption": ParagraphStyle(
            "VelesCaption",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10.5,
            textColor=theme.neutral,
            spaceBefore=5,
            spaceAfter=8,
        ),
        "source": ParagraphStyle(
            "VelesSource",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.4,
            leading=9.5,
            textColor=theme.muted,
            spaceBefore=3,
            spaceAfter=6,
        ),
        "callout_title": ParagraphStyle(
            "VelesCalloutTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=theme.primary,
            spaceAfter=4,
        ),
        "callout_body": ParagraphStyle(
            "VelesCalloutBody",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.8,
            leading=12.5,
            textColor=theme.body_text,
        ),
        "card_label": ParagraphStyle(
            "VelesCardLabel",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9,
            textColor=theme.neutral,
            spaceAfter=4,
        ),
        "card_value": ParagraphStyle(
            "VelesCardValue",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=20,
            textColor=theme.primary,
            spaceAfter=4,
        ),
        "card_note": ParagraphStyle(
            "VelesCardNote",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=6.8,
            leading=8.5,
            textColor=theme.neutral,
        ),
        "dashboard_subheading": ParagraphStyle(
            "VelesDashboardSubheading",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=theme.white,
        ),
        "dashboard_label": ParagraphStyle(
            "VelesDashboardLabel",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.7,
            leading=10.5,
            textColor=theme.neutral,
        ),
        "dashboard_value": ParagraphStyle(
            "VelesDashboardValue",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.7,
            leading=10.5,
            textColor=theme.primary,
        ),
        "executive_label": ParagraphStyle(
            "VelesExecutiveLabel",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.2,
            leading=9,
            tracking=0.7,
            textColor=theme.neutral,
        ),
        "executive_company": ParagraphStyle(
            "VelesExecutiveCompany",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=theme.primary,
        ),
        "executive_value": ParagraphStyle(
            "VelesExecutiveValue",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.2,
            leading=12,
            textColor=theme.body_text,
        ),
        "executive_business_model": ParagraphStyle(
            "VelesExecutiveBusinessModel",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=theme.body_text,
        ),
        "executive_panel_title": ParagraphStyle(
            "VelesExecutivePanelTitle",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.2,
            leading=11,
            textColor=theme.primary,
            spaceAfter=5,
        ),
        "executive_bullet": ParagraphStyle(
            "VelesExecutiveBullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=10.3,
            textColor=theme.body_text,
            leftIndent=0,
            firstLineIndent=0,
            spaceAfter=3,
        ),
        "executive_metric_label": ParagraphStyle(
            "VelesExecutiveMetricLabel",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=6.6,
            leading=8,
            tracking=0.4,
            textColor=theme.neutral,
            alignment=1,
            spaceAfter=3,
        ),
        "executive_metric_value": ParagraphStyle(
            "VelesExecutiveMetricValue",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11.2,
            leading=14,
            textColor=theme.primary,
            alignment=1,
        ),
        "table_header": ParagraphStyle(
            "VelesTableHeader",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.5,
            leading=9,
            textColor=theme.white,
            alignment=0,
            spaceBefore=0,
            spaceAfter=0,
        ),
        "table_cell": ParagraphStyle(
            "VelesTableCell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=9.6,
            textColor=theme.body_text,
            alignment=0,
            spaceBefore=0,
            spaceAfter=0,
        ),
        "table_cell_compact": ParagraphStyle(
            "VelesTableCellCompact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=6.8,
            leading=8.0,
            textColor=theme.body_text,
            alignment=0,
            spaceBefore=0,
            spaceAfter=0,
        ),
        "toc_title": ParagraphStyle(
            "VelesTOCTitle",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=19,
            leading=23,
            textColor=theme.primary,
            spaceAfter=14,
        ),
        "toc_item": ParagraphStyle(
            "VelesTOCItem",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=15,
            textColor=theme.body_text,
            leftIndent=2,
            spaceAfter=3,
        ),
    }
