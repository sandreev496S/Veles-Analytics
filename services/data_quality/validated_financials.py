from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Iterable, Iterator, Mapping

from services.data_quality.balance_sheet_resolver import (
    resolve_latest_balance_sheet,
)
from services.data_quality.validated_metric import (
    MetricConfidence,
    MetricSourceType,
    MetricValidationStatus,
    ValidatedMetric,
    derived_metric,
    metric_from_provider_value,
    metric_from_sec_fact,
    unavailable_metric,
    withheld_metric,
)


def _parse_datetime(
    value: Any,
) -> datetime | None:
    if not value:
        return None

    if isinstance(value, datetime):
        return value

    try:
        return datetime.fromisoformat(
            str(value).replace("Z", "+00:00")
        )
    except (TypeError, ValueError):
        return None


def _parse_date(
    value: Any,
) -> date | None:
    if not value:
        return None

    if isinstance(value, date):
        return value

    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def _safe_float(
    value: Any,
) -> float | None:
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


def _mapping(
    value: Any,
) -> Mapping[str, Any]:
    if isinstance(value, Mapping):
        return value

    return {}


def _company_facts(
    research: Mapping[str, Any],
) -> dict[str, Any]:
    sec = _mapping(research.get("sec"))
    company_facts = _mapping(
        sec.get("company_facts")
    )
    facts = company_facts.get("facts")

    if isinstance(facts, dict):
        return facts

    return {}


def _raw_market_metrics(
    research: Mapping[str, Any],
) -> Mapping[str, Any]:
    market = _mapping(research.get("market"))

    return _mapping(market.get("raw_metrics"))


def _market_as_of(
    research: Mapping[str, Any],
) -> datetime | None:
    market = _mapping(research.get("market"))

    return _parse_datetime(market.get("as_of"))


def _provider_metric(
    raw_metrics: Mapping[str, Any],
    key: str,
) -> Mapping[str, Any]:
    return _mapping(raw_metrics.get(key))


@dataclass(frozen=True, slots=True)
class ValidatedMetricRegistry:
    metrics: Mapping[str, ValidatedMetric]

    def __getitem__(
        self,
        metric_name: str,
    ) -> ValidatedMetric:
        return self.metrics[metric_name]

    def get(
        self,
        metric_name: str,
    ) -> ValidatedMetric | None:
        return self.metrics.get(metric_name)

    def __iter__(self) -> Iterator[str]:
        return iter(self.metrics)

    def values(
        self,
    ) -> Iterable[ValidatedMetric]:
        return self.metrics.values()

    def available(
        self,
    ) -> dict[str, ValidatedMetric]:
        return {
            name: metric
            for name, metric in self.metrics.items()
            if metric.is_available
        }

    def withheld(
        self,
    ) -> dict[str, ValidatedMetric]:
        return {
            name: metric
            for name, metric in self.metrics.items()
            if metric.is_withheld
        }

    def to_dict(self) -> dict[str, dict[str, Any]]:
        return {
            name: metric.to_dict()
            for name, metric in self.metrics.items()
        }


def build_validated_metric_registry(
    research: Mapping[str, Any],
) -> ValidatedMetricRegistry:
    metrics: dict[str, ValidatedMetric] = {}

    facts = _company_facts(research)
    balance_sheet = resolve_latest_balance_sheet(facts)

    raw_market = _raw_market_metrics(research)
    market_as_of = _market_as_of(research)

    share_price_data = _provider_metric(
        raw_market,
        "share_price",
    )
    share_price_value = _safe_float(
        share_price_data.get("value")
    )

    if share_price_value is not None:
        metrics["share_price"] = metric_from_provider_value(
            name="share_price",
            display_name="Share Price",
            value=share_price_value,
            unit=str(
                share_price_data.get("unit")
                or "USD"
            ),
            provider="Yahoo Finance",
            source_type=MetricSourceType.MARKET_PROVIDER,
            as_of=market_as_of,
            definition=share_price_data.get("definition"),
            confidence=MetricConfidence.HIGH,
            status=MetricValidationStatus.VERIFIED,
        )
    else:
        metrics["share_price"] = unavailable_metric(
            name="share_price",
            display_name="Share Price",
            unit="USD",
            reason="Current share price was not available.",
        )

    market_cap_data = _provider_metric(
        raw_market,
        "market_cap",
    )
    market_cap_value = _safe_float(
        market_cap_data.get("value")
    )

    if market_cap_value is not None:
        metrics["market_cap"] = metric_from_provider_value(
            name="market_cap",
            display_name="Market Capitalization",
            value=market_cap_value,
            unit=str(
                market_cap_data.get("unit")
                or "USD"
            ),
            provider="Yahoo Finance",
            source_type=MetricSourceType.MARKET_PROVIDER,
            as_of=market_as_of,
            definition=market_cap_data.get("definition"),
            confidence=MetricConfidence.HIGH,
            status=MetricValidationStatus.VERIFIED,
        )
    else:
        metrics["market_cap"] = unavailable_metric(
            name="market_cap",
            display_name="Market Capitalization",
            unit="USD",
            reason=(
                "Current equity market capitalization "
                "was not available."
            ),
        )

    provider_ev_data = _provider_metric(
        raw_market,
        "provider_enterprise_value",
    )
    provider_ev_value = _safe_float(
        provider_ev_data.get("value")
    )

    if provider_ev_value is not None:
        metrics["provider_enterprise_value"] = (
            metric_from_provider_value(
                name="provider_enterprise_value",
                display_name=(
                    "Provider Enterprise Value"
                ),
                value=provider_ev_value,
                unit=str(
                    provider_ev_data.get("unit")
                    or "USD"
                ),
                provider="Yahoo Finance",
                source_type=(
                    MetricSourceType.MARKET_PROVIDER
                ),
                as_of=market_as_of,
                definition=provider_ev_data.get(
                    "definition"
                ),
                confidence=MetricConfidence.MEDIUM,
                status=MetricValidationStatus.FALLBACK,
                warnings=(
                    "Provider enterprise value uses "
                    "provider-defined debt, cash, and "
                    "other adjustment inputs.",
                ),
            )
        )
    else:
        metrics["provider_enterprise_value"] = (
            unavailable_metric(
                name="provider_enterprise_value",
                display_name=(
                    "Provider Enterprise Value"
                ),
                unit="USD",
                reason=(
                    "Provider enterprise value was "
                    "not available."
                ),
            )
        )

    if balance_sheet is None:
        for name, display_name in (
            (
                "cash_and_cash_equivalents",
                "Cash and Cash Equivalents",
            ),
            (
                "cash_including_restricted_cash",
                "Cash Including Restricted Cash",
            ),
            (
                "stockholders_equity",
                "Stockholders' Equity",
            ),
            (
                "financial_debt",
                "Financial Debt",
            ),
            (
                "operating_lease_liabilities",
                "Operating Lease Liabilities",
            ),
        ):
            metrics[name] = unavailable_metric(
                name=name,
                display_name=display_name,
                unit="USD",
                reason=(
                    "A canonical SEC balance-sheet "
                    "period could not be resolved."
                ),
            )

        metrics["reconciled_enterprise_value"] = (
            withheld_metric(
                name="reconciled_enterprise_value",
                display_name=(
                    "Reconciled Enterprise Value"
                ),
                unit="USD",
                as_of=market_as_of,
                reason=(
                    "Enterprise value was withheld "
                    "because no canonical SEC "
                    "balance sheet was available."
                ),
            )
        )

        return ValidatedMetricRegistry(metrics=metrics)

    period_end = balance_sheet.period_end

    cash_metric = metric_from_sec_fact(
        name="cash_and_cash_equivalents",
        display_name="Cash and Cash Equivalents",
        fact=(
            balance_sheet
            .cash_and_cash_equivalents
        ),
    )
    metrics[cash_metric.name] = cash_metric

    restricted_cash_fact = (
        balance_sheet
        .cash_including_restricted_cash
    )

    if restricted_cash_fact is not None:
        restricted_cash_metric = metric_from_sec_fact(
            name="cash_including_restricted_cash",
            display_name=(
                "Cash Including Restricted Cash"
            ),
            fact=restricted_cash_fact,
        )
    else:
        restricted_cash_metric = unavailable_metric(
            name="cash_including_restricted_cash",
            display_name=(
                "Cash Including Restricted Cash"
            ),
            unit="USD",
            reason=(
                "No period-aligned SEC restricted-cash "
                "fact was available."
            ),
        )

    metrics[
        restricted_cash_metric.name
    ] = restricted_cash_metric

    equity_fact = balance_sheet.stockholders_equity

    if equity_fact is not None:
        equity_metric = metric_from_sec_fact(
            name="stockholders_equity",
            display_name="Stockholders' Equity",
            fact=equity_fact,
        )
    else:
        equity_metric = unavailable_metric(
            name="stockholders_equity",
            display_name="Stockholders' Equity",
            unit="USD",
            reason=(
                "No period-aligned SEC stockholders' "
                "equity fact was available."
            ),
        )

    metrics[equity_metric.name] = equity_metric

    operating_lease_value = (
        balance_sheet.operating_lease_liabilities
    )

    if operating_lease_value is not None:
        lease_dependencies = tuple(
            metric_from_sec_fact(
                name=name,
                display_name=display_name,
                fact=fact,
            )
            for name, display_name, fact in (
                (
                    "operating_lease_current",
                    "Current Operating Lease Liability",
                    balance_sheet
                    .operating_lease_current,
                ),
                (
                    "operating_lease_noncurrent",
                    (
                        "Noncurrent Operating "
                        "Lease Liability"
                    ),
                    balance_sheet
                    .operating_lease_noncurrent,
                ),
            )
            if fact is not None
        )

        lease_metric = derived_metric(
            name="operating_lease_liabilities",
            display_name=(
                "Operating Lease Liabilities"
            ),
            value=operating_lease_value,
            unit="USD",
            formula=(
                "current operating lease liability "
                "+ noncurrent operating lease liability"
            ),
            dependencies=lease_dependencies,
            period_end=period_end,
        )
    else:
        lease_metric = unavailable_metric(
            name="operating_lease_liabilities",
            display_name=(
                "Operating Lease Liabilities"
            ),
            unit="USD",
            reason=(
                "Both current and noncurrent "
                "period-aligned operating lease "
                "components were not available."
            ),
        )

    metrics[lease_metric.name] = lease_metric

    if (
        balance_sheet.total_financial_debt
        is not None
    ):
        debt_metric = metric_from_sec_fact(
            name="financial_debt",
            display_name="Financial Debt",
            fact=balance_sheet.total_financial_debt,
        )
    elif (
        balance_sheet
        .resolved_financial_debt_components
    ):
        component_metrics = tuple(
            metric_from_sec_fact(
                name=(
                    "financial_debt_component_"
                    f"{index}"
                ),
                display_name=(
                    "Financial Debt Component"
                ),
                fact=fact,
            )
            for index, fact in enumerate(
                balance_sheet
                .resolved_financial_debt_components,
                start=1,
            )
        )

        debt_metric = withheld_metric(
            name="financial_debt",
            display_name="Financial Debt",
            unit="USD",
            period_end=period_end,
            reason=(
                "Financial debt components were "
                "partially resolved, but completeness "
                "could not be established."
            ),
            dependencies=component_metrics,
        )
    else:
        debt_metric = withheld_metric(
            name="financial_debt",
            display_name="Financial Debt",
            unit="USD",
            period_end=period_end,
            reason=(
                "No period-aligned SEC financial-debt "
                "fact was available."
            ),
        )

    metrics[debt_metric.name] = debt_metric

    market_cap_metric = metrics["market_cap"]

    if (
        market_cap_metric.value is not None
        and debt_metric.value is not None
        and balance_sheet.debt_is_safe_for_ev
    ):
        reconciled_ev = (
            market_cap_metric.value
            + debt_metric.value
            - cash_metric.value
        )

        metrics["reconciled_enterprise_value"] = (
            derived_metric(
                name="reconciled_enterprise_value",
                display_name=(
                    "Reconciled Enterprise Value"
                ),
                value=reconciled_ev,
                unit="USD",
                formula=(
                    "market capitalization "
                    "+ financial debt "
                    "- cash and cash equivalents"
                ),
                dependencies=(
                    market_cap_metric,
                    debt_metric,
                    cash_metric,
                ),
                period_end=period_end,
                as_of=market_as_of,
                warnings=(
                    "Market capitalization is current "
                    "while cash and debt reflect the "
                    "latest reported balance-sheet date.",
                ),
            )
        )
    else:
        reasons: list[str] = []

        if market_cap_metric.value is None:
            reasons.append(
                "market capitalization was unavailable"
            )

        if debt_metric.value is None:
            reasons.append(
                "period-aligned financial debt "
                "was unresolved"
            )

        if not balance_sheet.debt_is_safe_for_ev:
            reasons.append(
                "financial debt was not validated "
                "as complete"
            )

        reason_text = "; ".join(dict.fromkeys(reasons))

        metrics["reconciled_enterprise_value"] = (
            withheld_metric(
                name="reconciled_enterprise_value",
                display_name=(
                    "Reconciled Enterprise Value"
                ),
                unit="USD",
                period_end=period_end,
                as_of=market_as_of,
                reason=(
                    "Enterprise value was withheld "
                    f"because {reason_text}."
                ),
                dependencies=(
                    market_cap_metric,
                    debt_metric,
                    cash_metric,
                ),
            )
        )

    return ValidatedMetricRegistry(metrics=metrics)
