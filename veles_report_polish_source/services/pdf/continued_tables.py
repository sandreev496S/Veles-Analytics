from __future__ import annotations

from copy import deepcopy
from typing import Any, Sequence

from reportlab.lib import colors
from reportlab.platypus import LongTable, TableStyle

from services.pdf.theme import PDFTheme, VELES_PDF_THEME


class ContinuedLongTable(LongTable):
    """
    Repeats a title and column header when a table spans multiple pages.

    Row 0: title row
    Row 1: column headers
    Rows 2+: data
    """

    def __init__(
        self,
        title: str,
        data: Sequence[Sequence[Any]],
        *,
        col_widths=None,
        theme: PDFTheme = VELES_PDF_THEME,
        **kwargs,
    ) -> None:
        self.continued_title = f"{title} — Continued"
        self.original_title = title
        self.theme = theme

        if not data:
            data = [[""]]

        column_count = max(len(row) for row in data)

        title_row = [title] + [""] * (column_count - 1)
        table_data = [title_row] + [list(row) for row in data]

        super().__init__(
            table_data,
            colWidths=col_widths,
            repeatRows=2,
            hAlign="LEFT",
            **kwargs,
        )

        self._apply_style(column_count)

    def _apply_style(self, column_count: int) -> None:
        self.setStyle(
            TableStyle(
                [
                    ("SPAN", (0, 0), (-1, 0)),
                    ("BACKGROUND", (0, 0), (-1, 0), self.theme.card_background),
                    ("TEXTCOLOR", (0, 0), (-1, 0), self.theme.primary),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("TOPPADDING", (0, 0), (-1, 0), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 7),

                    ("BACKGROUND", (0, 1), (-1, 1), self.theme.primary),
                    ("TEXTCOLOR", (0, 1), (-1, 1), colors.white),
                    ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),

                    ("FONTNAME", (0, 2), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 1), (-1, -1), 8),
                    ("GRID", (0, 1), (-1, -1), 0.25, self.theme.light_border),
                    ("BOX", (0, 0), (-1, -1), 0.4, self.theme.border),
                    ("ROWBACKGROUNDS", (0, 2), (-1, -1), [
                        colors.white,
                        self.theme.light_background,
                    ]),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 6),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                    ("TOPPADDING", (0, 1), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 1), (-1, -1), 5),
                ]
            )
        )

    def split(self, availWidth, availHeight):
        fragments = super().split(availWidth, availHeight)

        for index, fragment in enumerate(fragments):
            if index == 0:
                continue

            try:
                fragment._cellvalues[0][0] = self.continued_title
            except Exception:
                pass

        return fragments
