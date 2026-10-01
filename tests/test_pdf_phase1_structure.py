from __future__ import annotations

import ast
from pathlib import Path


EXPORTER_PATH = Path("services/pdf_report_exporter.py")


def _source() -> str:
    return EXPORTER_PATH.read_text(encoding="utf-8")


def test_pdf_exporter_is_valid_python():
    ast.parse(_source())


def test_report_has_one_toc_builder():
    source = _source()

    assert source.count("build_automatic_toc(") == 1


def test_report_has_one_executive_summary_renderer():
    source = _source()

    assert source.count(
        "build_executive_summary_page("
    ) == 1

    assert (
        'section_header_bar(\n'
        '                "Executive Summary"'
    ) not in source


def test_opening_report_order():
    source = _source()

    cover = source.index(
        "build_cover("
    )
    toc = source.index(
        "build_automatic_toc("
    )
    summary = source.index(
        "build_executive_summary_page("
    )
    dashboard = source.index(
        "build_dashboard_v2(",
        summary,
    )
    snapshot = source.index(
        '"Company Snapshot"',
        dashboard,
    )

    assert cover < toc < summary < dashboard < snapshot


def test_executive_summary_does_not_create_blank_leading_page():
    source = _source()

    summary_start = source.index(
        "build_executive_summary_page("
    )
    summary_end = source.index(
        ")\n    )",
        summary_start,
    )

    summary_call = source[
        summary_start:summary_end
    ]

    assert "include_page_break=False" in summary_call


def test_dashboard_has_explicit_page_boundary():
    source = _source()

    summary = source.index(
        "build_executive_summary_page("
    )
    dashboard = source.index(
        "build_dashboard_v2(",
        summary,
    )

    between = source[summary:dashboard]

    assert "story.append(PageBreak())" in between


def test_company_snapshot_does_not_repeat_investment_conclusions():
    source = _source()

    snapshot_start = source.index(
        "# Company Snapshot"
    )
    charts_start = source.index(
        "# Financial and market charts",
        snapshot_start,
    )

    snapshot_block = source[
        snapshot_start:charts_start
    ]

    assert 'Paragraph("Investment Thesis"' not in snapshot_block
    assert 'Paragraph("Key Risks"' not in snapshot_block
    assert 'report.get("thesis_points"' not in snapshot_block
    assert 'report.get("risks"' not in snapshot_block
