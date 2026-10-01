from __future__ import annotations

from typing import Any, Iterable
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from services.pdf.sections import section_header_bar
from services.pdf.theme import PDFTheme, VELES_PDF_THEME


def _summary_payload(
    report: Any,
) -> dict[str, Any]:
    """
    Retrieve the structured executive summary from either a
    dictionary-compatible ReportDocument or a plain dictionary.
    """
    if isinstance(report, dict):
        payload = report.get(
            "executive_summary",
            {},
        )
    else:
        payload = getattr(
            report,
            "executive_summary",
            {},
        )

    return payload if isinstance(payload, dict) else {}


def _safe_text(
    value: Any,
    default: str = "Not available",
) -> str:
    text = str(value or "").strip()

    if text in {
        "",
        "None",
        "N/A",
        "Unknown",
    }:
        return default

    return text


def _bullet_paragraphs(
    items: Iterable[Any],
    styles: dict,
    *,
    maximum: int = 4,
) -> list[Paragraph]:
    rendered: list[Paragraph] = []

    for item in list(items)[:maximum]:
        text = _safe_text(
            item,
            "",
        )

        if not text:
            continue

        rendered.append(
            Paragraph(
                (
                    '<font color="#1D4ED8">'
                    "&#8226;"
                    "</font> "
                    f"{escape(text)}"
                ),
                styles["executive_bullet"],
            )
        )

    if not rendered:
        rendered.append(
            Paragraph(
                "No material items were identified.",
                styles["executive_bullet"],
            )
        )

    return rendered


def _identity_block(
    summary: dict[str, Any],
    styles: dict,
    *,
    theme: PDFTheme,
):
    company = _safe_text(
        summary.get("company"),
    )
    industry = _safe_text(
        summary.get("industry"),
    )
    business_model = _safe_text(
        summary.get("business_model"),
    )

    rows = [
        [
            Paragraph(
                "COMPANY",
                styles["executive_label"],
            ),
            Paragraph(
                escape(company),
                styles["executive_company"],
            ),
        ],
        [
            Paragraph(
                "INDUSTRY",
                styles["executive_label"],
            ),
            Paragraph(
                escape(industry),
                styles["executive_value"],
            ),
        ],
        [
            Paragraph(
                "BUSINESS MODEL",
                styles["executive_label"],
            ),
            Paragraph(
                escape(business_model),
                styles["executive_business_model"],
            ),
        ],
    ]

    table = Table(
        rows,
        colWidths=[
            1.18 * inch,
            theme.content_width - 1.18 * inch,
        ],
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    theme.light_background,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.6,
                    theme.border,
                ),
                (
                    "LINEBELOW",
                    (0, 0),
                    (-1, -2),
                    0.35,
                    theme.light_border,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    return table


def _list_panel(
    title: str,
    items: Iterable[Any],
    styles: dict,
    *,
    width: float,
    accent: colors.Color,
    theme: PDFTheme,
):
    content = [
        Paragraph(
            escape(title),
            styles["executive_panel_title"],
        ),
        *_bullet_paragraphs(
            items,
            styles,
        ),
    ]

    table = Table(
        [[content]],
        colWidths=[width],
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    theme.white,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    theme.light_border,
                ),
                (
                    "LINEABOVE",
                    (0, 0),
                    (-1, 0),
                    3,
                    accent,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    return table


def _financial_snapshot(
    summary: dict[str, Any],
    styles: dict,
    *,
    theme: PDFTheme,
):
    snapshot = summary.get(
        "financial_snapshot",
        {},
    )

    if not isinstance(snapshot, dict):
        snapshot = {}

    preferred_order = [
        "Revenue",
        "Cash",
        "Debt",
        "Net Income",
        "Free Cash Flow",
        "Indicative Cash Runway",
    ]

    metrics = [
        (
            label,
            _safe_text(
                snapshot.get(label),
                "N/A",
            ),
        )
        for label in preferred_order
    ]

    cells = []

    for label, value in metrics:
        cells.append(
            [
                Paragraph(
                    escape(label.upper()),
                    styles["executive_metric_label"],
                ),
                Paragraph(
                    escape(value),
                    styles["executive_metric_value"],
                ),
            ]
        )

    row_one = [
        Table(
            [[cells[index]]],
            colWidths=[
                theme.content_width / 3
                - 0.08 * inch
            ],
        )
        for index in range(3)
    ]

    row_two = [
        Table(
            [[cells[index]]],
            colWidths=[
                theme.content_width / 3
                - 0.08 * inch
            ],
        )
        for index in range(3, 6)
    ]

    table = Table(
        [
            row_one,
            row_two,
        ],
        colWidths=[
            theme.content_width / 3
        ] * 3,
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    theme.card_background,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    theme.border,
                ),
                (
                    "INNERGRID",
                    (0, 0),
                    (-1, -1),
                    0.35,
                    theme.light_border,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    return table


def build_executive_summary_page(
    report: Any,
    styles: dict,
    *,
    include_page_break: bool = True,
    theme: PDFTheme = VELES_PDF_THEME,
) -> list:
    """
    Build a structured, institutional-style executive summary.

    The component is intentionally based entirely on the assembled
    report payload. It performs no external data retrieval and does
    not generate new analytical claims.
    """
    summary = _summary_payload(report)

    elements: list = []

    if include_page_break:
        elements.append(
            PageBreak()
        )

    elements.append(
        section_header_bar(
            "Executive Summary",
            styles,
            subtitle=(
                "Company profile, investment considerations, "
                "financial position, and principal risks"
            ),
            anchor="executive_summary",
            theme=theme,
        )
    )

    elements.append(
        _identity_block(
            summary,
            styles,
            theme=theme,
        )
    )

    elements.append(
        Spacer(
            1,
            0.12 * inch,
        )
    )

    panel_gap = 0.08 * inch
    column_width = (
        theme.content_width - panel_gap
    ) / 2

    highlights = _list_panel(
        "Key Investment Considerations",
        summary.get(
            "investment_highlights",
            [],
        ),
        styles,
        width=column_width,
        accent=theme.positive,
        theme=theme,
    )

    risks = _list_panel(
        "Key Risks",
        summary.get(
            "key_risks",
            [],
        ),
        styles,
        width=column_width,
        accent=theme.negative,
        theme=theme,
    )

    two_column = Table(
        [[highlights, risks]],
        colWidths=[
            column_width,
            column_width,
        ],
        hAlign="LEFT",
    )

    two_column.setStyle(
        TableStyle(
            [
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    panel_gap / 2,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    panel_gap / 2,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    0,
                ),
            ]
        )
    )

    elements.append(
        KeepTogether(
            [two_column]
        )
    )

    elements.append(
        Spacer(
            1,
            0.12 * inch,
        )
    )

    elements.append(
        _financial_snapshot(
            summary,
            styles,
            theme=theme,
        )
    )

    catalysts = summary.get(
        "key_catalysts",
        [],
    )

    if catalysts:
        elements.append(
            Spacer(
                1,
                0.12 * inch,
            )
        )

        elements.append(
            _list_panel(
                "Potential Catalysts",
                catalysts,
                styles,
                width=theme.content_width,
                accent=theme.secondary,
                theme=theme,
            )
        )

    return elements
