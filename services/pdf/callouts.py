from __future__ import annotations

from typing import Literal
from xml.sax.saxutils import escape

from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Table, TableStyle

from services.pdf.theme import PDFTheme, VELES_PDF_THEME


CalloutType = Literal[
    "neutral",
    "positive",
    "negative",
    "warning",
    "insight",
]


def analyst_callout(
    title: str,
    body: str,
    styles: dict,
    *,
    callout_type: CalloutType = "neutral",
    width: float | None = None,
    theme: PDFTheme = VELES_PDF_THEME,
):
    accent_map = {
        "neutral": theme.neutral,
        "positive": theme.positive,
        "negative": theme.negative,
        "warning": theme.warning,
        "insight": theme.secondary,
    }

    background_map = {
        "neutral": theme.light_background,
        "positive": theme.light_background,
        "negative": theme.light_background,
        "warning": theme.light_background,
        "insight": theme.card_background,
    }

    accent = accent_map[callout_type]
    background = background_map[callout_type]
    resolved_width = width or theme.content_width

    title_style = styles["callout_title"].clone(
        f"{title}_CalloutTitle"
    )
    body_style = styles["callout_body"].clone(
        f"{title}_CalloutBody"
    )

    # Smaller type is necessary for side-by-side institutional callouts.
    if resolved_width < 2.5 * inch:
        title_style.fontSize = 8.4
        title_style.leading = 10
        body_style.fontSize = 7.5
        body_style.leading = 9.6

    content = [
        Paragraph(
            escape(str(title)),
            title_style,
        ),
        Paragraph(
            escape(str(body)).replace("\n", "<br/>"),
            body_style,
        ),
    ]

    table = Table(
        [[content]],
        colWidths=[resolved_width],
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), background),
                ("BOX", (0, 0), (-1, -1), 0.45, theme.light_border),
                ("LINEBEFORE", (0, 0), (0, -1), 4, accent),
                ("LEFTPADDING", (0, 0), (-1, -1), 9),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 9),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    return table


def three_column_callouts(
    left: tuple[str, str, CalloutType],
    middle: tuple[str, str, CalloutType],
    right: tuple[str, str, CalloutType],
    styles: dict,
    *,
    theme: PDFTheme = VELES_PDF_THEME,
):
    outer_column_width = theme.content_width / 3
    gutter = 0.06 * inch
    inner_width = outer_column_width - (2 * gutter)

    cards = [
        analyst_callout(
            title,
            body,
            styles,
            callout_type=callout_type,
            width=inner_width,
            theme=theme,
        )
        for title, body, callout_type in [left, middle, right]
    ]

    table = Table(
        [[cards[0], cards[1], cards[2]]],
        colWidths=[
            outer_column_width,
            outer_column_width,
            outer_column_width,
        ],
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), gutter),
                ("RIGHTPADDING", (0, 0), (-1, -1), gutter),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    return table
