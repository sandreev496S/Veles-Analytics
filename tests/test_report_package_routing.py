from __future__ import annotations

from unittest.mock import patch

from services.equity_report_engine import (
    build_equity_report_from_ticker_v2,
)
from services.reports.profiles import (
    BASIC_REPORT_PROFILE,
    PROFESSIONAL_REPORT_PROFILE,
)
from services.reports.report_service import assemble_report


@patch(
    "services.reports.report_service."
    "assemble_equity_report"
)
def test_report_service_routes_basic_ticker_report(
    mock_assemble,
):
    mock_assemble.return_value = object()

    assemble_report(
        "RXRX",
        package="Basic",
    )

    mock_assemble.assert_called_once_with(
        "RXRX",
        profile=BASIC_REPORT_PROFILE,
    )


@patch(
    "services.reports.report_service."
    "assemble_equity_report"
)
def test_report_service_defaults_ticker_to_professional(
    mock_assemble,
):
    mock_assemble.return_value = object()

    assemble_report("RXRX")

    mock_assemble.assert_called_once_with(
        "RXRX",
        profile=PROFESSIONAL_REPORT_PROFILE,
    )


@patch(
    "services.equity_report_engine."
    "assemble_equity_report"
)
def test_legacy_engine_routes_basic_package(
    mock_assemble,
):
    mock_assemble.return_value = object()

    build_equity_report_from_ticker_v2(
        "RXRX",
        package="Basic",
    )

    mock_assemble.assert_called_once_with(
        "RXRX",
        profile=BASIC_REPORT_PROFILE,
    )


@patch(
    "services.equity_report_engine."
    "assemble_equity_report"
)
def test_legacy_engine_defaults_to_professional(
    mock_assemble,
):
    mock_assemble.return_value = object()

    build_equity_report_from_ticker_v2(
        "RXRX"
    )

    mock_assemble.assert_called_once_with(
        "RXRX",
        profile=PROFESSIONAL_REPORT_PROFILE,
    )


@patch(
    "services.reports.report_service."
    "assemble_equity_report"
)
def test_starter_alias_routes_to_basic(
    mock_assemble,
):
    mock_assemble.return_value = object()

    assemble_report(
        "RXRX",
        package="starter",
    )

    mock_assemble.assert_called_once_with(
        "RXRX",
        profile=BASIC_REPORT_PROFILE,
    )
