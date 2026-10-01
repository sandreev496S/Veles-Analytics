from services.pdf.document import VelesReportDocument
from services.pdf.figures import figure_anchor, figure_reference
from services.pdf.sections import slugify_anchor


def test_section_anchor_is_stable():
    assert slugify_anchor("Financial Overview") == "financial_overview"
    assert slugify_anchor("SEC Filings Snapshot") == "sec_filings_snapshot"


def test_figure_anchor_and_reference():
    assert figure_anchor(3) == "figure_3"
    assert 'href="#figure_3"' in figure_reference(3)


def test_document_class_exists():
    assert VelesReportDocument.__name__ == "VelesReportDocument"
