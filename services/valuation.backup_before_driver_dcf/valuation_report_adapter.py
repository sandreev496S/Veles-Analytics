from __future__ import annotations

from typing import Any

from services.valuation.integration_validation import (
    DCFIntegrationError,
    validate_complete_dcf_payload,
)


def _money(value: float | None) -> str:
    if value is None:
        return "N/A"

    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}B"

    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"

    return f"${value:,.2f}"


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

        table.append([
            name.title(),
            _money(scenario.get("enterprise_value")),
            _money(scenario.get("equity_value")),
            (
                f"${scenario.get('implied_value_per_share', 0):,.2f}"
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
            _money(year.get("revenue")),
            _percent(year.get("revenue_growth")),
            _percent(year.get("ebit_margin")),
            _money(year.get("ebit")),
            _money(year.get("unlevered_fcf")),
            _money(year.get("present_value_fcf")),
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

    return [
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
            "Cash",
            _money(assumptions.get("cash")),
            "Observed",
        ],
        [
            "Debt",
            _money(assumptions.get("debt")),
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
        return {
            "status": "invalid",
            "method": "Enterprise DCF",
            "message": str(exc),
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

    warnings = (
        payload.get("assumption_build", {})
        .get("warnings", [])
    )

    current_price = (
        payload.get("snapshot", {})
        .get("share_price", {})
        .get("value")
    )

    implied_value = base.get(
        "implied_value_per_share"
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
            "enterprise_value": _money(
                base.get("enterprise_value")
            ),
            "equity_value": _money(
                base.get("equity_value")
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
            "pv_forecast_fcf": _money(
                base.get(
                    "present_value_forecast_fcf"
                )
            ),
            "pv_terminal_value": _money(
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
        "warnings": warnings,
        "raw": payload,
    }
