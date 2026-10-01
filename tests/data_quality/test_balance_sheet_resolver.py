from datetime import date

from services.data_quality.balance_sheet_resolver import (
    resolve_latest_balance_sheet,
)
from services.data_quality.sec_facts import (
    SECPeriodKind,
    select_sec_fact,
)


def _fact(
    *,
    end: str,
    value: float,
    form: str = "10-Q",
    fp: str = "Q1",
) -> dict:
    return {
        "fy": int(end[:4]),
        "fp": fp,
        "form": form,
        "filed": end,
        "end": end,
        "value": value,
    }


def test_target_period_prevents_stale_fallback():
    facts = {
        "LongTermDebt": [
            _fact(
                end="2021-12-31",
                value=723_000,
                form="10-K",
                fp="FY",
            )
        ]
    }

    result = select_sec_fact(
        facts,
        concepts=("LongTermDebt",),
        period_kind=SECPeriodKind.INSTANT,
        target_period_end=date(2026, 3, 31),
    )

    assert result is None


def test_balance_sheet_anchors_to_latest_cash():
    facts = {
        "CashAndCashEquivalentsAtCarryingValue": [
            _fact(
                end="2026-03-31",
                value=654_473_000,
            )
        ],
        "StockholdersEquity": [
            _fact(
                end="2026-03-31",
                value=1_024_769_000,
            )
        ],
        "FinanceLeaseLiabilityCurrent": [
            _fact(
                end="2025-12-31",
                value=8_967_000,
                form="10-K",
                fp="FY",
            )
        ],
    }

    result = resolve_latest_balance_sheet(facts)

    assert result is not None
    assert result.period_end == date(2026, 3, 31)
    assert (
        result.cash_and_cash_equivalents.value
        == 654_473_000
    )
    assert result.stockholders_equity is not None

    # The stale 2025 finance lease must not be imported.
    assert result.finance_lease_current is None
    assert result.gross_financial_debt is None
    assert result.debt_resolution_status == "unresolved"
    assert not result.debt_is_safe_for_ev


def test_operating_leases_require_both_components():
    facts = {
        "CashAndCashEquivalentsAtCarryingValue": [
            _fact(
                end="2026-03-31",
                value=654_473_000,
            )
        ],
        "OperatingLeaseLiabilityCurrent": [
            _fact(
                end="2026-03-31",
                value=13_087_000,
            )
        ],
        "OperatingLeaseLiabilityNoncurrent": [
            _fact(
                end="2026-03-31",
                value=42_842_000,
            )
        ],
    }

    result = resolve_latest_balance_sheet(facts)

    assert result is not None
    assert (
        result.operating_lease_liabilities
        == 55_929_000
    )


def test_old_debt_is_never_mixed_with_current_cash():
    facts = {
        "CashAndCashEquivalentsAtCarryingValue": [
            _fact(
                end="2026-03-31",
                value=654_473_000,
            )
        ],
        "NotesPayableCurrent": [
            _fact(
                end="2024-03-31",
                value=55_000,
            )
        ],
        "LongTermDebt": [
            _fact(
                end="2021-12-31",
                value=723_000,
                form="10-K",
                fp="FY",
            )
        ],
    }

    result = resolve_latest_balance_sheet(facts)

    assert result is not None
    assert result.current_financial_debt is None
    assert result.total_financial_debt is None
    assert result.gross_financial_debt is None
