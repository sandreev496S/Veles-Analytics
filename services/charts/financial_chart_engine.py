from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


BRAND_DARK = "#0F172A"
BRAND_BLUE = "#1D4ED8"
BRAND_LIGHT_BLUE = "#60A5FA"
BRAND_GRAY = "#64748B"
BRAND_RED = "#B91C1C"
BRAND_GREEN = "#15803D"
GRID_COLOR = "#CBD5E1"


def _parse_number(value: Any) -> float | None:
    if value is None:
        return None

    text = str(value).strip().replace("$", "").replace(",", "")

    if text in {"", "N/A", "None", "Unknown"}:
        return None

    multiplier = 1.0

    if text.endswith("B"):
        multiplier = 1_000_000_000
        text = text[:-1]
    elif text.endswith("M"):
        multiplier = 1_000_000
        text = text[:-1]
    elif text.endswith("K"):
        multiplier = 1_000
        text = text[:-1]

    try:
        return float(text) * multiplier
    except ValueError:
        return None


def _year_label(value: Any) -> str:
    text = str(value)

    match = re.search(r"(20\d{2})", text)
    if match:
        return match.group(1)

    return text


def _statement_series(
    table: list[list[Any]],
    metric: str,
) -> tuple[list[str], list[float]]:
    if not table or len(table) < 2:
        return [], []

    headers = [_year_label(item) for item in table[0][1:]]

    row = next(
        (
            item
            for item in table[1:]
            if item and str(item[0]).strip() == metric
        ),
        None,
    )

    if not row:
        return [], []

    pairs: list[tuple[str, float]] = []

    for label, raw_value in zip(headers, row[1:]):
        value = _parse_number(raw_value)

        if value is not None:
            pairs.append((label, value / 1_000_000))

    # Yahoo statement tables generally arrive newest first.
    pairs.reverse()

    return (
        [pair[0] for pair in pairs],
        [pair[1] for pair in pairs],
    )


def _latest_table_value(
    table: list[list[Any]],
    metric: str,
) -> float | None:
    for row in table[1:]:
        if row and str(row[0]).strip() == metric and len(row) > 1:
            return _parse_number(row[1])

    return None


def _market_value(
    market_snapshot: list[list[Any]],
    metric: str,
) -> float | None:
    for row in market_snapshot[1:]:
        if row and str(row[0]).strip() == metric and len(row) > 1:
            return _parse_number(row[1])

    return None


def _finish_chart(
    fig,
    ax,
    output_path: Path,
    ylabel: str,
) -> str:
    ax.set_ylabel(
        ylabel,
        fontsize=8,
        color=BRAND_GRAY,
        labelpad=8,
    )

    ax.tick_params(
        axis="x",
        labelsize=8,
        colors=BRAND_GRAY,
        length=0,
    )
    ax.tick_params(
        axis="y",
        labelsize=8,
        colors=BRAND_GRAY,
        length=0,
    )

    ax.grid(
        axis="y",
        alpha=0.55,
        color=GRID_COLOR,
        linewidth=0.55,
    )
    ax.set_axisbelow(True)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(GRID_COLOR)
    ax.spines["bottom"].set_linewidth(0.7)

    ax.margins(x=0.12)

    fig.tight_layout(pad=1.1)
    fig.savefig(
        output_path,
        dpi=220,
        bbox_inches="tight",
        facecolor="white",
        edgecolor="none",
    )
    plt.close(fig)

    return str(output_path)


def _bar_chart(
    labels: list[str],
    values: list[float],
    title: str,
    output_path: Path,
    color: str,
    ylabel: str = "USD ($M)",
) -> str | None:
    if not labels or not values:
        return None

    fig, ax = plt.subplots(figsize=(7.2, 3.05))
    bars = ax.bar(labels, values, color=color, width=0.58)
    # Chart title supplied by PDF figure heading.

    for bar, value in zip(bars, values):
        ax.annotate(
            f"{value:,.0f}" if float(value).is_integer() else f"{value:,.1f}",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 5 if value >= 0 else -14),
            textcoords="offset points",
            ha="center",
            va="bottom" if value >= 0 else "top",
            fontsize=7.5,
            color=BRAND_DARK,
        )

    return _finish_chart(fig, ax, output_path, ylabel)


def _loss_chart(
    labels: list[str],
    operating_values: list[float],
    net_values: list[float],
    output_path: Path,
    operating_color: str,
    net_color: str,
) -> str | None:
    if not labels or not operating_values or not net_values:
        return None

    fig, ax = plt.subplots(figsize=(7.2, 3.05))

    positions = list(range(len(labels)))
    width = 0.34

    ax.bar(
        [position - width / 2 for position in positions],
        operating_values,
        width=width,
        label="Operating income/loss",
        color=operating_color,
    )
    ax.bar(
        [position + width / 2 for position in positions],
        net_values,
        width=width,
        label="Net income/loss",
        color=net_color,
    )

    ax.set_xticks(positions)
    ax.set_xticklabels(labels)
    # Chart title supplied by PDF figure heading.

    ax.axhline(
        0,
        linewidth=0.8,
        color=GRID_COLOR,
        zorder=0,
    )

    ax.legend(
        frameon=False,
        fontsize=7.5,
        loc="best",
        ncol=2,
    )

    return _finish_chart(
        fig,
        ax,
        output_path,
        "USD ($M)",
    )



def _comparison_chart(
    labels: list[str],
    values: list[float],
    title: str,
    output_path: Path,
    colors: list[str],
    ylabel: str,
) -> str | None:
    if not labels or not values:
        return None

    fig, ax = plt.subplots(figsize=(7.2, 3.05))
    bars = ax.bar(
        labels,
        values,
        color=colors,
        width=0.58,
    )
    # Chart title supplied by PDF figure heading.

    for bar, value in zip(bars, values):
        ax.annotate(
            f"{value:,.0f}" if float(value).is_integer() else f"{value:,.1f}",
            xy=(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
            ),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=7.5,
            color=BRAND_DARK,
        )

    return _finish_chart(
        fig,
        ax,
        output_path,
        ylabel,
    )


def generate_financial_charts(
    ticker: str,
    income_statement: list[list[Any]],
    balance_sheet: list[list[Any]],
    market_snapshot: list[list[Any]],
    report_brand: dict[str, Any] | None = None,
    brand: dict[str, Any] | None = None,
    output_root: str = "reports/generated/charts",
) -> dict[str, str]:
    ticker = ticker.upper().strip()

    # `brand` remains supported for backward compatibility.
    palette = report_brand or brand or {}

    primary = palette.get("primary", BRAND_DARK)
    secondary = palette.get("secondary", BRAND_BLUE)
    accent = palette.get("accent", BRAND_LIGHT_BLUE)
    positive = palette.get("positive", BRAND_GREEN)
    negative = palette.get("negative", BRAND_RED)
    warning = palette.get("warning", "#D97706")
    neutral = palette.get("neutral", BRAND_GRAY)

    output_dir = Path(output_root) / ticker.lower()
    output_dir.mkdir(parents=True, exist_ok=True)

    charts: dict[str, str] = {}

    revenue_labels, revenue_values = _statement_series(
        income_statement,
        "Revenue",
    )
    revenue_path = _bar_chart(
        revenue_labels,
        revenue_values,
        "Revenue Trend",
        output_dir / "revenue_trend.png",
        secondary,
    )
    if revenue_path:
        charts["revenue_trend"] = revenue_path

    rd_labels, rd_values = _statement_series(
        income_statement,
        "R&D Expense",
    )
    rd_path = _bar_chart(
        rd_labels,
        rd_values,
        "Research & Development Expense Trend",
        output_dir / "rd_expense_trend.png",
        accent,
    )
    if rd_path:
        charts["rd_expense_trend"] = rd_path

    operating_labels, operating_values = _statement_series(
        income_statement,
        "Operating Income",
    )
    net_labels, net_values = _statement_series(
        income_statement,
        "Net Income",
    )

    if operating_labels == net_labels:
        loss_path = _loss_chart(
            operating_labels,
            operating_values,
            net_values,
            output_dir / "operating_net_loss_trend.png",
            operating_color=negative,
            net_color=neutral,
        )
        if loss_path:
            charts["operating_net_loss_trend"] = loss_path

    cash = _latest_table_value(
        balance_sheet,
        "Cash & Equivalents",
    )
    debt = _latest_table_value(
        balance_sheet,
        "Total Debt",
    )

    if cash is not None and debt is not None:
        cash_debt_path = _comparison_chart(
            labels=["Cash", "Debt"],
            values=[cash / 1_000_000, debt / 1_000_000],
            title="Cash Versus Debt",
            output_path=output_dir / "cash_vs_debt.png",
            colors=[positive, warning],
            ylabel="USD ($M)",
        )
        if cash_debt_path:
            charts["cash_vs_debt"] = cash_debt_path

    market_cap = _market_value(
        market_snapshot,
        "Market Cap",
    )
    enterprise_value = _market_value(
        market_snapshot,
        "Enterprise Value",
    )

    if market_cap is not None and enterprise_value is not None:
        market_value_path = _comparison_chart(
            labels=["Market Cap", "Enterprise Value"],
            values=[
                market_cap / 1_000_000_000,
                enterprise_value / 1_000_000_000,
            ],
            title="Market Capitalization Versus Enterprise Value",
            output_path=output_dir / "market_cap_vs_ev.png",
            colors=[primary, secondary],
            ylabel="USD billions",
        )
        if market_value_path:
            charts["market_cap_vs_ev"] = market_value_path

    return charts
