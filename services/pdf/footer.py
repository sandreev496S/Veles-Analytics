from __future__ import annotations

from reportlab.lib.units import inch

from services.pdf.theme import PDFTheme, VELES_PDF_THEME


def draw_report_footer(
    canvas,
    doc,
    *,
    report_type: str = "Equity Research",
    confidentiality: str = "",
    theme: PDFTheme = VELES_PDF_THEME,
) -> None:
    canvas.saveState()

    canvas.setStrokeColor(theme.border)
    canvas.line(
        theme.margin_left,
        0.55 * inch,
        theme.page_width - theme.margin_right,
        0.55 * inch,
    )

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(theme.neutral)

    left_text = f"Veles Analytics | {report_type}"

    if confidentiality:
        left_text += f" | {confidentiality}"

    canvas.drawString(
        theme.margin_left,
        0.35 * inch,
        left_text,
    )

    canvas.drawRightString(
        theme.page_width - theme.margin_right,
        0.35 * inch,
        f"Page {doc.page}",
    )

    canvas.restoreState()


def make_footer_callback(
    *,
    report_type: str = "Equity Research",
    confidentiality: str = "",
    theme: PDFTheme = VELES_PDF_THEME,
):
    def callback(canvas, doc) -> None:
        draw_report_footer(
            canvas,
            doc,
            report_type=report_type,
            confidentiality=confidentiality,
            theme=theme,
        )

    return callback
