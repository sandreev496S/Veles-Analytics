from __future__ import annotations

from typing import Any

from services.analysis.financial_metrics import (
    BalanceSheetState,
    build_financial_metrics,
)

from services.utils.formatting import (
    format_precise_money,
)

from services.valuation.integration_validation import (
    DCFIntegrationError,
    validate_complete_dcf_payload,
)



def _percent(value: float | None) -> str:
    if value is None:
        return "N/A"

    return f"{value:.1%}"


def _scenario_table(
    scenarios: dict[str, dict[str, Any]],
) -> list[list[Any]]:
    table: list[list[Any]] = [
        [
            "Scenario",
            "Enterprise Value",
            "Equity Value",
            "Implied Value / Share",
        ]
    ]

    order = ["bull", "base", "bear"]

    for name in order:
        scenario = scenarios.get(name)

        if not scenario:
            continue

        raw_enterprise_value = scenario.get(
            "enterprise_value"
        )
        raw_equity_value = scenario.get(
            "equity_value"
        )

        displayed_enterprise_value = (
            max(raw_enterprise_value, 0.0)
            if raw_enterprise_value is not None
            else None
        )
        displayed_equity_value = (
            max(raw_equity_value, 0.0)
            if raw_equity_value is not None
            else None
        )

        table.append([
            name.title(),
            format_precise_money(displayed_enterprise_value),
            format_precise_money(displayed_equity_value),
            (
                f"${max(
                    scenario.get(
                        'implied_value_per_share',
                        0,
                    ),
                    0.0,
                ):,.2f}"
            ),
        ])

    return table


def _forecast_table(
    forecast: list[dict[str, Any]],
) -> list[list[Any]]:
    table: list[list[Any]] = [[
        "Year",
        "Revenue",
        "Growth",
        "EBIT Margin",
        "EBIT",
        "Unlevered FCF",
        "PV of FCF",
    ]]

    for year in forecast:
        table.append([
            year.get("year"),
            format_precise_money(
                year.get(
                    "total_revenue",
                    year.get("revenue"),
                )
            ),
            _percent(year.get("revenue_growth")),
            _percent(year.get("ebit_margin")),
            format_precise_money(year.get("ebit")),
            format_precise_money(year.get("unlevered_fcf")),
            format_precise_money(year.get("present_value_fcf")),
        ])

    return table


def _sensitivity_table(
    sensitivity: dict[str, Any] | None,
) -> list[list[Any]]:
    if not sensitivity:
        return []

    wacc_values = sensitivity.get(
        "wacc_values",
        [],
    )
    terminal_values = sensitivity.get(
        "terminal_growth_values",
        [],
    )

    cell_map = {
        (
            cell.get("wacc"),
            cell.get("terminal_growth_rate"),
        ): cell.get("implied_value_per_share")
        for cell in sensitivity.get("cells", [])
    }

    table: list[list[Any]] = [
        ["WACC / Terminal Growth"]
        + [_percent(value) for value in terminal_values]
    ]

    for wacc in wacc_values:
        row: list[Any] = [_percent(wacc)]

        for terminal_growth in terminal_values:
            value = cell_map.get(
                (wacc, terminal_growth)
            )

            row.append(
                f"${value:,.2f}"
                if value is not None
                else "N/A"
            )

        table.append(row)

    return table


def _assumption_table(
    result: dict[str, Any],
) -> list[list[Any]]:
    build = result.get(
        "assumption_build",
        {},
    )

    assumptions = build.get(
        "assumptions",
        {},
    )

    base_result = result.get(
        "base_result",
        {},
    )

    forecast = base_result.get(
        "forecast",
        [],
    )

    terminal_ebit_margin = None

    if forecast:
        terminal_ebit_margin = forecast[-1].get(
            "ebit_margin"
        )

    table = [
        ["Assumption", "Value", "Classification"],
        [
            "Risk-Free Rate",
            _percent(
                assumptions.get("risk_free_rate")
            ),
            "Analyst assumption",
        ],
        [
            "Equity Risk Premium",
            _percent(
                assumptions.get("equity_risk_premium")
            ),
            "Analyst assumption",
        ],
        [
            "Beta",
            f"{assumptions.get('beta', 0):.2f}",
            "Observed or analyst override",
        ],
        [
            "Pre-Tax Cost of Debt",
            _percent(
                assumptions.get("cost_of_debt")
            ),
            "Analyst assumption",
        ],
        [
            "Debt Weight",
            _percent(
                assumptions.get("debt_weight")
            ),
            "Analyst assumption",
        ],
        [
            "Equity Weight",
            _percent(
                assumptions.get("equity_weight")
            ),
            "Analyst assumption",
        ],
        [
            "Terminal Growth Rate",
            _percent(
                assumptions.get("terminal_growth_rate")
            ),
            "Analyst assumption",
        ],
        [
            "Terminal-Year EBIT Margin",
            _percent(terminal_ebit_margin),
            "Derived model output",
        ],
        [
            "Cash",
            format_precise_money(assumptions.get("cash")),
            "Observed",
        ],
        [
            "Debt",
            format_precise_money(assumptions.get("debt")),
            "Observed",
        ],
        [
            "Diluted Shares",
            (
                f"{assumptions.get('diluted_shares_outstanding', 0):,.0f}"
            ),
            "Observed or derived",
        ],
    ]

    return table


def _build_review_flags(
    payload: dict[str, Any],
    base: dict[str, Any],
    scenarios: dict[str, dict[str, Any]],
    warnings: list[str],
) -> list[dict[str, str]]:
    flags: list[dict[str, str]] = []
    used_categories: set[str] = set()

    def add_flag(
        *,
        category: str,
        status: str,
        tone: str,
        item: str,
    ) -> None:
        if category in used_categories:
            return

        used_categories.add(category)
        flags.append({
            "category": category,
            "status": status,
            "tone": tone,
            "item": item,
        })

    assumptions = base.get("assumptions", {})
    forecast = base.get("forecast", [])

    cash = assumptions.get("cash")
    debt = assumptions.get("debt")


    financial_metrics = build_financial_metrics(
        cash=cash,
        debt=debt,
    )

    if (
        financial_metrics.balance_sheet_state
        is BalanceSheetState.NET_CASH
    ):
        add_flag(
            category="net_cash",
            status="Positive",
            tone="positive",
            item=(
                "The company enters the model with a net-cash "
                "balance."
            ),
        )
    elif (
        financial_metrics.balance_sheet_state
        is BalanceSheetState.NET_DEBT
    ):
        add_flag(
            category="net_debt",
            status="Review",
            tone="warning",
            item=(
                "The company enters the model with a net-debt "
                "balance."
            ),
        )

    terminal_margin = (
        forecast[-1].get("ebit_margin")
        if forecast
        else None
    )

    if (
        terminal_margin is not None
        and terminal_margin > 0.40
    ):
        add_flag(
            category="terminal_margin",
            status="Review",
            tone="warning",
            item=(
                "Terminal-year EBIT margin exceeds 40%; "
                "review mature-state revenue and expense assumptions."
            ),
        )

    first_positive_ebit_year = next(
        (
            row.get("year")
            for row in forecast
            if (
                row.get("ebit") is not None
                and row.get("ebit") > 0
            )
        ),
        None,
    )

    if first_positive_ebit_year is not None:
        add_flag(
            category="profitability_transition",
            status="Review",
            tone="warning",
            item=(
                "The model first reaches positive EBIT in "
                f"{first_positive_ebit_year}."
            ),
        )

    bull = scenarios.get(
        "bull",
        {},
    ).get(
        "implied_value_per_share"
    )
    base_value = scenarios.get(
        "base",
        {},
    ).get(
        "implied_value_per_share"
    )
    bear = scenarios.get(
        "bear",
        {},
    ).get(
        "implied_value_per_share"
    )

    if (
        bull is not None
        and base_value is not None
        and bear is not None
        and bull >= base_value >= bear
    ):
        add_flag(
            category="scenario_monotonicity",
            status="Passed",
            tone="positive",
            item=(
                "Scenario monotonicity passed: "
                "Bull ≥ Base ≥ Bear."
            ),
        )

    if payload.get("model_status") == "illustrative":
        add_flag(
            category="illustrative_model",
            status="Review",
            tone="warning",
            item=(
                "This remains an illustrative scenario model "
                "and is not a final investment valuation."
            ),
        )

    for warning in warnings:
        normalized = str(warning).strip().lower()

        if not normalized:
            continue

        if (
            "terminal-year ebit margin" in normalized
            or (
                "terminal" in normalized
                and "margin" in normalized
                and "40%" in normalized
            )
        ):
            category = "terminal_margin"
        elif (
            "illustrative" in normalized
            or "not a final valuation" in normalized
            or "not a final investment valuation" in normalized
        ):
            category = "illustrative_model"
        elif (
            "scenario monotonicity" in normalized
            or "bull" in normalized
            and "base" in normalized
            and "bear" in normalized
        ):
            category = "scenario_monotonicity"
        elif "net-cash" in normalized or "net cash" in normalized:
            category = "net_cash"
        elif "net-debt" in normalized or "net debt" in normalized:
            category = "net_debt"
        elif (
            "positive ebit" in normalized
            or "profitability" in normalized
        ):
            category = "profitability_transition"
        else:
            category = (
                "warning:"
                + normalized.replace(" ", "_")[:80]
            )

        add_flag(
            category=category,
            status="Review",
            tone="warning",
            item=str(warning).strip(),
        )

    return flags


def adapt_saved_valuation_for_report(
    saved_valuation: dict[str, Any] | None,
) -> dict[str, Any]:
    if not saved_valuation:
        return {
            "status": "unavailable",
            "method": "Enterprise DCF",
            "message": (
                "No saved valuation model is available "
                "for this ticker."
            ),
        }

    payload = saved_valuation.get("payload", {})

    try:
        validate_complete_dcf_payload(payload)
    except DCFIntegrationError as exc:
        message = str(exc)

        missing_layers: list[str] = []

        prefix = "Incomplete DCF payload. Missing: "

        if message.startswith(prefix):
            missing_layers = [
                item.strip()
                for item in message[len(prefix):].split(",")
                if item.strip()
            ]

        return {
            "status": "invalid",
            "method": "Enterprise DCF",
            "message": message,
            "missing_layers": missing_layers,
        }

    base = payload.get("base_result", {})
    scenarios = payload.get("scenarios", {})
    sensitivity = payload.get("sensitivity")
    assumption_build = payload.get(
        "assumption_build",
        {},
    )

    missing_layers = []

    if not base:
        missing_layers.append("base_result")

    if not base.get("forecast"):
        missing_layers.append("base_result.forecast")

    if not scenarios:
        missing_layers.append("scenarios")

    if not sensitivity:
        missing_layers.append("sensitivity")

    if not assumption_build.get("assumptions"):
        missing_layers.append(
            "assumption_build.assumptions"
        )

    if missing_layers:
        return {
            "status": "invalid",
            "method": "Enterprise DCF",
            "message": (
                "The saved valuation is incomplete. "
                "Missing layers: "
                + ", ".join(missing_layers)
            ),
            "missing_layers": missing_layers,
        }

    if not base:
        return {
            "status": "invalid",
            "method": "Enterprise DCF",
            "message": (
                "The saved valuation does not contain "
                "a base DCF result."
            ),
        }

    warnings = list(
        payload.get(
            "assumption_build",
            {},
        ).get(
            "warnings",
            [],
        )
    )

    review_flags = _build_review_flags(
        payload,
        base,
        scenarios,
        warnings,
    )

    current_price = (
        payload.get("snapshot", {})
        .get("share_price", {})
        .get("value")
    )

    raw_enterprise_value = base.get(
        "enterprise_value"
    )
    raw_equity_value = base.get(
        "equity_value"
    )
    raw_implied_value = base.get(
        "implied_value_per_share"
    )

    displayed_enterprise_value = (
        max(raw_enterprise_value, 0.0)
        if raw_enterprise_value is not None
        else None
    )
    displayed_equity_value = (
        max(raw_equity_value, 0.0)
        if raw_equity_value is not None
        else None
    )
    implied_value = (
        max(raw_implied_value, 0.0)
        if raw_implied_value is not None
        else None
    )

    zero_floor_applied = any(
        value is not None and value < 0
        for value in [
            raw_enterprise_value,
            raw_equity_value,
            raw_implied_value,
        ]
    )

    implied_upside = None

    if (
        current_price is not None
        and implied_value is not None
        and current_price > 0
    ):
        implied_upside = (
            implied_value / current_price - 1
        )

    return {
        "status": "available",
        "method": "Enterprise DCF",
        "name": saved_valuation.get(
            "name",
            "Saved DCF",
        ),
        "saved_at": saved_valuation.get(
            "saved_at",
        ),
        "assumption_source": (
            "Analyst-edited assumptions combined "
            "with observed Veles data"
        ),
        "summary": {
            "enterprise_value": format_precise_money(
                displayed_enterprise_value
            ),
            "equity_value": format_precise_money(
                displayed_equity_value
            ),
            "implied_value_per_share": (
                f"${implied_value:,.2f}"
                if implied_value is not None
                else "N/A"
            ),
            "current_share_price": (
                f"${current_price:,.2f}"
                if current_price is not None
                else "N/A"
            ),
            "implied_upside": (
                _percent(implied_upside)
                if implied_upside is not None
                else "N/A"
            ),
            "wacc": _percent(
                base.get("wacc")
            ),
            "terminal_growth_rate": _percent(
                base.get(
                    "assumptions",
                    {},
                ).get(
                    "terminal_growth_rate"
                )
            ),
            "pv_forecast_fcf": format_precise_money(
                base.get(
                    "present_value_forecast_fcf"
                )
            ),
            "pv_terminal_value": format_precise_money(
                base.get(
                    "present_value_terminal_value"
                )
            ),
        },
        "scenario_table": _scenario_table(
            scenarios
        ),
        "forecast_table": _forecast_table(
            base.get("forecast", [])
        ),
        "sensitivity_table": _sensitivity_table(
            sensitivity
        ),
        "assumption_table": _assumption_table(
            payload
        ),
        "model_status": payload.get(
            "model_status",
            "illustrative",
        ),
        "model_note": payload.get(
            "model_note",
            (
                "Illustrative analytical scenario. "
                "Not a final investment valuation."
            ),
        ),
        "forecast_years": payload.get(
            "forecast_years",
            len(base.get("forecast", [])),
        ),
        "zero_floor_applied": zero_floor_applied,
        "raw_values": {
            "enterprise_value": raw_enterprise_value,
            "equity_value": raw_equity_value,
            "implied_value_per_share": raw_implied_value,
        },
        "review_flags": review_flags,
        "warnings": (
            warnings
            + (
                [
                    (
                        "The raw model produced a negative operating or "
                        "equity value. Professional presentation applies "
                        "a $0.00 floor; raw values remain stored in the "
                        "saved model."
                    )
                ]
                if zero_floor_applied
                else []
            )
        ),
        "raw": payload,
    }
