from __future__ import annotations

from typing import Any
from xml.sax.saxutils import escape

from reportlab.platypus import Paragraph, Table, TableStyle

from services.pdf.theme import PDFTheme, VELES_PDF_THEME


def metric_card(
    metric: dict[str, Any],
    styles: dict,
    *,
    width: float,
    height: float,
    theme: PDFTheme = VELES_PDF_THEME,
):
    label = escape(str(metric.get("label", "Metric")))
    value = escape(str(metric.get("value", "N/A")))
    note = escape(str(metric.get("note", "")))

    content = [
        Paragraph(label, styles["card_label"]),
        Paragraph(value, styles["card_value"]),
        Paragraph(note, styles["card_note"]),
    ]

    card = Table(
        [[content]],
        colWidths=[width],
        rowHeights=[height],
    )

    card.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), theme.card_background),
                ("BOX", (0, 0), (-1, -1), 0.6, theme.border),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    return card


def key_value_panel(
    title: str,
    values: dict[str, Any],
    styles: dict,
    *,
    label_width: float,
    value_width: float,
    theme: PDFTheme = VELES_PDF_THEME,
):
    rows = [
        [
            Paragraph(
                escape(title),
                styles["dashboard_subheading"],
            ),
            "",
        ]
    ]

    for key, value in values.items():
        rows.append(
            [
                Paragraph(
                    escape(str(key)),
                    styles["dashboard_label"],
                ),
                Paragraph(
                    escape(str(value)),
                    styles["dashboard_value"],
                ),
            ]
        )

    panel = Table(
        rows,
        colWidths=[label_width, value_width],
    )

    panel.setStyle(
        TableStyle(
            [
                ("SPAN", (0, 0), (1, 0)),
                ("BACKGROUND", (0, 0), (1, 0), theme.primary),
                ("BOX", (0, 0), (-1, -1), 0.5, theme.border),
                ("INNERGRID", (0, 1), (-1, -1), 0.25, theme.border),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    return panel
