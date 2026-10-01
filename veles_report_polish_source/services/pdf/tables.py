from __future__ import annotations

from typing import Any, Sequence

from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from services.pdf.theme import PDFTheme, VELES_PDF_THEME


def build_table(
    data: Sequence[Sequence[Any]],
    col_widths: Sequence[float] | None = None,
    *,
    repeat_header: bool = True,
    numeric_columns: set[int] | None = None,
    first_column_bold: bool = False,
    compact: bool = False,
    theme: PDFTheme = VELES_PDF_THEME,
):
    if not data:
        return Spacer(1, 1)

    table = Table(
        data,
        colWidths=col_widths,
        repeatRows=1 if repeat_header else 0,
        hAlign="LEFT",
    )

    font_size = 7.8 if compact else 8.2
    vertical_padding = 4 if compact else 5.5

    commands: list[tuple] = [
        ("BACKGROUND", (0, 0), (-1, 0), theme.primary),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "LEFT"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("TEXTCOLOR", (0, 1), (-1, -1), theme.body_text),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, theme.primary),
        ("INNERGRID", (0, 1), (-1, -1), 0.2, theme.light_border),
        ("BOX", (0, 0), (-1, -1), 0.4, theme.border),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        (
            "ROWBACKGROUNDS",
            (0, 1),
            (-1, -1),
            [colors.white, theme.light_background],
        ),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), vertical_padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1), vertical_padding),
    ]

    if first_column_bold:
        commands.append(
            ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold")
        )

    for column in numeric_columns or set():
        commands.extend(
            [
                ("ALIGN", (column, 0), (column, -1), "RIGHT"),
                (
                    "FONTNAME",
                    (column, 1),
                    (column, -1),
                    "Helvetica",
                ),
            ]
        )

    table.setStyle(TableStyle(commands))
    return table
