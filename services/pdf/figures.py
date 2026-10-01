from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.units import inch
from reportlab.platypus import (
    AnchorFlowable,
    Image,
    KeepTogether,
    Paragraph,
    Spacer,
)

from services.pdf.theme import PDFTheme, VELES_PDF_THEME


def figure_anchor(figure_number: int) -> str:
    return f"figure_{figure_number}"


def figure_reference(figure_number: int) -> str:
    return (
        f'<a href="#{figure_anchor(figure_number)}">'
        f"Figure {figure_number}</a>"
    )


def report_figure(
    image_path: str,
    *,
    figure_number: int,
    title: str,
    styles: dict,
    width: float = 6.7 * inch,
    height: float = 3.05 * inch,
    commentary: str = "",
    source: str = "",
    theme: PDFTheme = VELES_PDF_THEME,
):
    path = Path(image_path)

    if not path.exists():
        return Spacer(1, 1)

    anchor = figure_anchor(figure_number)

    title_paragraph = Paragraph(
        (
            f"<b>Figure {figure_number}.</b> "
            f"{escape(str(title))}"
        ),
        styles["h2"],
    )

    items = [
        # AnchorFlowable creates a real PDF destination on the canvas.  A
        # Paragraph <a name=...> marker can be lost during ReportLab's
        # multi-pass layout, leaving otherwise valid figure links unresolved.
        AnchorFlowable(anchor),
        title_paragraph,
        Image(
            str(path),
            width=width,
            height=height,
        ),
    ]

    if commentary:
        items.append(
            Paragraph(
                escape(str(commentary)),
                styles["caption"],
            )
        )

    if source:
        items.append(
            Paragraph(
                f"Source: {escape(str(source))}",
                styles["source"],
            )
        )

    items.append(
        Spacer(
            1,
            theme.figure_gap,
        )
    )

    return KeepTogether(items)
