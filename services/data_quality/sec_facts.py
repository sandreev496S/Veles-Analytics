from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Any, Iterable


class SECPeriodKind(str, Enum):
    INSTANT = "instant"
    ANNUAL = "annual"
    QUARTER = "quarter"


@dataclass(frozen=True, slots=True)
class ResolvedSECFact:
    concept: str
    value: float
    unit: str
    form: str
    fiscal_year: int | None
    fiscal_period: str | None
    period_start: date | None
    period_end: date
    filing_date: date | None
    accession_number: str | None
    frame: str | None
    source_name: str = "SEC EDGAR companyfacts API"

    @property
    def provenance_key(self) -> str:
        accession = self.accession_number or "unknown-accession"
        return (
            f"{self.concept}:"
            f"{self.period_end.isoformat()}:"
            f"{accession}"
        )


def _parse_date(value: Any) -> date | None:
    if not value:
        return None

    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def _safe_float(value: Any) -> float | None:
    if value is None:
        return None

    try:
        number = float(value)
    except (TypeError, ValueError):
        return None

    if number != number:
        return None

    if number in {
        float("inf"),
        float("-inf"),
    }:
        return None

    return number


def _normalized_form(value: Any) -> str:
    return str(value or "").upper().strip()


def _normalized_fp(value: Any) -> str:
    return str(value or "").upper().strip()


def _is_annual_record(record: dict[str, Any]) -> bool:
    return (
        _normalized_form(record.get("form"))
        in {"10-K", "20-F", "40-F"}
        and _normalized_fp(record.get("fp"))
        == "FY"
    )


def _is_quarter_record(record: dict[str, Any]) -> bool:
    return (
        _normalized_form(record.get("form"))
        in {"10-Q", "6-K"}
        and _normalized_fp(record.get("fp"))
        in {"Q1", "Q2", "Q3"}
    )


def _is_periodic_record(record: dict[str, Any]) -> bool:
    return _normalized_form(record.get("form")) in {
        "10-K",
        "10-Q",
        "20-F",
        "40-F",
        "6-K",
    }


def _record_sort_key(
    record: dict[str, Any],
) -> tuple[date, date, int]:
    period_end = _parse_date(record.get("end")) or date.min
    filed = _parse_date(record.get("filed")) or date.min

    form = _normalized_form(record.get("form"))
    form_priority = {
        "10-Q": 5,
        "10-K": 4,
        "20-F": 4,
        "40-F": 4,
        "6-K": 3,
    }.get(form, 0)

    return (
        period_end,
        filed,
        form_priority,
    )


def _deduplicate_records(
    records: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    Remove duplicate SEC observations while preserving the latest
    filing for a given concept period and fiscal designation.
    """
    best: dict[
        tuple[str, str, str],
        dict[str, Any],
    ] = {}

    for record in records:
        end = str(record.get("end") or "")
        fp = _normalized_fp(record.get("fp"))
        form = _normalized_form(record.get("form"))

        key = (
            end,
            fp,
            form,
        )

        current = best.get(key)

        if (
            current is None
            or _record_sort_key(record)
            > _record_sort_key(current)
        ):
            best[key] = record

    return list(best.values())


def select_sec_fact(
    facts: dict[str, Any],
    *,
    concepts: Iterable[str],
    period_kind: SECPeriodKind,
    unit: str = "USD",
    target_period_end: date | None = None,
) -> ResolvedSECFact | None:
    """
    Select one deterministic SEC fact from an ordered concept list.

    Concept order is significant: the first concept with a valid
    matching observation wins.
    """
    for concept in concepts:
        raw_records = facts.get(concept, [])

        if not isinstance(raw_records, list):
            continue

        records = _deduplicate_records(
            record
            for record in raw_records
            if isinstance(record, dict)
        )

        if period_kind is SECPeriodKind.ANNUAL:
            records = [
                record
                for record in records
                if _is_annual_record(record)
            ]
        elif period_kind is SECPeriodKind.QUARTER:
            records = [
                record
                for record in records
                if _is_quarter_record(record)
            ]
        else:
            records = [
                record
                for record in records
                if _is_periodic_record(record)
            ]

        valid: list[dict[str, Any]] = []

        for record in records:
            period_end = _parse_date(
                record.get("end")
            )

            if period_end is None:
                continue

            if (
                target_period_end is not None
                and period_end != target_period_end
            ):
                continue

            if _safe_float(record.get("value")) is None:
                continue

            valid.append(record)

        if not valid:
            continue

        selected = max(
            valid,
            key=_record_sort_key,
        )

        value = _safe_float(selected.get("value"))
        period_end = _parse_date(selected.get("end"))

        if value is None or period_end is None:
            continue

        fiscal_year_raw = selected.get("fy")

        try:
            fiscal_year = (
                int(fiscal_year_raw)
                if fiscal_year_raw is not None
                else None
            )
        except (TypeError, ValueError):
            fiscal_year = None

        return ResolvedSECFact(
            concept=concept,
            value=value,
            unit=unit,
            form=_normalized_form(
                selected.get("form")
            ),
            fiscal_year=fiscal_year,
            fiscal_period=(
                _normalized_fp(selected.get("fp"))
                or None
            ),
            period_start=_parse_date(
                selected.get("start")
            ),
            period_end=period_end,
            filing_date=_parse_date(
                selected.get("filed")
            ),
            accession_number=(
                str(
                    selected.get(
                        "accession_number"
                    )
                )
                if selected.get(
                    "accession_number"
                )
                else None
            ),
            frame=(
                str(selected.get("frame"))
                if selected.get("frame")
                else None
            ),
        )

    return None


def select_sec_series(
    facts: dict[str, Any],
    *,
    concepts: Iterable[str],
    period_kind: SECPeriodKind,
    max_periods: int = 3,
    unit: str = "USD",
) -> list[ResolvedSECFact]:
    """
    Select a deterministic historical series from the first concept
    containing valid observations.
    """
    for concept in concepts:
        raw_records = facts.get(concept, [])

        if not isinstance(raw_records, list):
            continue

        records = _deduplicate_records(
            record
            for record in raw_records
            if isinstance(record, dict)
        )

        if period_kind is SECPeriodKind.ANNUAL:
            records = [
                record
                for record in records
                if _is_annual_record(record)
            ]
        elif period_kind is SECPeriodKind.QUARTER:
            records = [
                record
                for record in records
                if _is_quarter_record(record)
            ]
        else:
            records = [
                record
                for record in records
                if _is_periodic_record(record)
            ]

        selected_by_end: dict[
            date,
            dict[str, Any],
        ] = {}

        for record in records:
            period_end = _parse_date(
                record.get("end")
            )
            value = _safe_float(
                record.get("value")
            )

            if period_end is None or value is None:
                continue

            current = selected_by_end.get(period_end)

            if (
                current is None
                or _record_sort_key(record)
                > _record_sort_key(current)
            ):
                selected_by_end[period_end] = record

        if not selected_by_end:
            continue

        ordered = sorted(
            selected_by_end.values(),
            key=_record_sort_key,
            reverse=True,
        )[:max_periods]

        result: list[ResolvedSECFact] = []

        for record in ordered:
            value = _safe_float(record.get("value"))
            period_end = _parse_date(record.get("end"))

            if value is None or period_end is None:
                continue

            fiscal_year_raw = record.get("fy")

            try:
                fiscal_year = (
                    int(fiscal_year_raw)
                    if fiscal_year_raw is not None
                    else None
                )
            except (TypeError, ValueError):
                fiscal_year = None

            result.append(
                ResolvedSECFact(
                    concept=concept,
                    value=value,
                    unit=unit,
                    form=_normalized_form(
                        record.get("form")
                    ),
                    fiscal_year=fiscal_year,
                    fiscal_period=(
                        _normalized_fp(
                            record.get("fp")
                        )
                        or None
                    ),
                    period_start=_parse_date(
                        record.get("start")
                    ),
                    period_end=period_end,
                    filing_date=_parse_date(
                        record.get("filed")
                    ),
                    accession_number=(
                        str(
                            record.get(
                                "accession_number"
                            )
                        )
                        if record.get(
                            "accession_number"
                        )
                        else None
                    ),
                    frame=(
                        str(record.get("frame"))
                        if record.get("frame")
                        else None
                    ),
                )
            )

        return result

    return []
