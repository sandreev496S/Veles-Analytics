from pathlib import Path

import pytest

from scripts.generate_fixture_sample_report import build_report
from services.pdf_report_exporter import export_equity_report_pdf_v2
from services.reports.reconciliation import validate_report_for_delivery

pytestmark = pytest.mark.e2e


def test_fixture_sample_report_reconciles_and_exports(tmp_path: Path):
    report = build_report(tmp_path)
    assert validate_report_for_delivery(report) == []
    assert report["dashboard_metrics"][0]["value"] == "$20.00"
    assert report["valuation"]["summary"]["current_share_price"] == "$20.00"
    output = tmp_path / "sample.pdf"
    export_equity_report_pdf_v2(report, output)
    assert output.exists()
    assert output.stat().st_size > 50_000
