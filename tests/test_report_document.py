from services.reports.equity_report_assembler import assemble_equity_report
from services.reports.models import ReportDocument


def test_assembler_returns_report_document():
    report = assemble_equity_report("RXRX")

    assert isinstance(report, ReportDocument)
    assert report.ticker == "RXRX"
    assert report.company_name
    assert len(report.dashboard_metrics) >= 6


def test_report_document_dictionary_compatibility():
    report = assemble_equity_report("RXRX")

    assert report["ticker"] == "RXRX"
    assert report.get("company_name")
    assert "dashboard_metrics" in report
