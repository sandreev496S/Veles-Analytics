from __future__ import annotations

from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

from services.pdf.theme import PDFTheme, VELES_PDF_THEME


class VelesReportDocument(BaseDocTemplate):
    """
    Multi-pass document supporting:
    - automatic table of contents
    - named section anchors
    - accurate page references
    """

    def __init__(
        self,
        filename: str,
        *,
        footer_callback,
        theme: PDFTheme = VELES_PDF_THEME,
        **kwargs,
    ) -> None:
        super().__init__(
            filename,
            pagesize=letter,
            leftMargin=theme.margin_left,
            rightMargin=theme.margin_right,
            topMargin=theme.margin_top,
            bottomMargin=theme.margin_bottom,
            **kwargs,
        )

        frame = Frame(
            self.leftMargin,
            self.bottomMargin,
            self.width,
            self.height,
            id="main_frame",
        )

        template = PageTemplate(
            id="main",
            frames=[frame],
            onPage=footer_callback,
        )

        self.addPageTemplates([template])

    def afterFlowable(self, flowable) -> None:
        """
        Register headings with ReportLab's TOC during multiBuild().
        """
        level = getattr(flowable, "_veles_toc_level", None)
        title = getattr(flowable, "_veles_toc_title", None)
        anchor = getattr(flowable, "_veles_anchor", None)

        if level is None or not title:
            return

        page_number = self.page

        if anchor:
            self.notify(
                "TOCEntry",
                (level, title, page_number, anchor),
            )
        else:
            self.notify(
                "TOCEntry",
                (level, title, page_number),
            )
