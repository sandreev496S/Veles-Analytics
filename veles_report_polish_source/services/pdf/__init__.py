from services.pdf.appendix import build_professional_appendix
from services.pdf.callouts import analyst_callout, three_column_callouts
from services.pdf.cards import key_value_panel, metric_card
from services.pdf.continued_tables import ContinuedLongTable
from services.pdf.cover import build_cover
from services.pdf.dashboard import build_dashboard_v2
from services.pdf.document import VelesReportDocument
from services.pdf.executive_summary import build_executive_summary_page
from services.pdf.figures import (
    figure_anchor,
    figure_reference,
    report_figure,
)
from services.pdf.footer import draw_report_footer, make_footer_callback
from services.pdf.sections import (
    anchored_heading,
    cross_reference,
    narrative_section,
    section_header_bar,
    section_heading,
    slugify_anchor,
    subsection_heading,
)
from services.pdf.tables import build_table
from services.pdf.theme import (
    PDFTheme,
    VELES_PDF_THEME,
    build_pdf_styles,
)
from services.pdf.toc import build_automatic_toc

__all__ = [
    "PDFTheme",
    "VELES_PDF_THEME",
    "VelesReportDocument",
    "build_pdf_styles",
    "build_cover",
    "build_dashboard_v2",
    "build_executive_summary_page",
    "build_automatic_toc",
    "build_table",
    "ContinuedLongTable",
    "metric_card",
    "key_value_panel",
    "analyst_callout",
    "three_column_callouts",
    "section_heading",
    "subsection_heading",
    "section_header_bar",
    "anchored_heading",
    "slugify_anchor",
    "cross_reference",
    "narrative_section",
    "report_figure",
    "figure_anchor",
    "figure_reference",
    "draw_report_footer",
    "make_footer_callback",
    "build_professional_appendix",
    "build_valuation_section",
]

from services.pdf.valuation import build_valuation_section
