from reportlab.platypus import Paragraph
from reportlab.platypus.tableofcontents import TableOfContents

from services.pdf.toc import build_automatic_toc
from services.pdf.theme import build_pdf_styles


def test_automatic_toc_component_builds():
    styles = build_pdf_styles()

    elements = build_automatic_toc(styles)

    assert len(elements) == 3
    assert isinstance(elements[0], Paragraph)
    assert isinstance(elements[2], TableOfContents)


def test_plain_ampersands_are_not_double_escaped():
    from services.pdf_report_exporter import (
        _clean_text,
        _paragraph_text,
    )

    assert _clean_text("R&amp;D") == "R&D"
    assert _clean_text("Cash &amp; Equivalents") == "Cash & Equivalents"
    assert _paragraph_text("R&D") == "R&amp;D"


def test_financial_abbreviations_do_not_gain_semicolons():
    from services.pdf_report_exporter import _clean_text

    assert _clean_text("R&D; spending") == "R&D spending"
    assert _clean_text("SG&A; expense") == "SG&A expense"
    assert _clean_text("R&amp;D; expense") == "R&D expense"
    assert _clean_text("SG&amp;A; expense") == "SG&A expense"
