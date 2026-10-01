from __future__ import annotations

from typing import Any

from services.utils.formatting import (
    format_report_money,
)

from services.reports.analyst_assessment import (
    build_financial_assessment,
)
from services.reports.analyst_interpretation import (
    development_risks,
    interpret_balance_sheet_position,
    interpret_balance_sheet_risk,
    interpret_cash_burn_risk,
    interpret_cash_position,
    interpret_profitability_risk,
    interpret_research_investment,
    interpret_revenue_growth,
)



def _numeric_statement_series(
    table: list[list[Any]],
    metric: str,
) -> list[float]:
    """
    Temporary historical-series compatibility path.

    Only raw numeric observations are accepted. Formatted display strings are
    not converted back into financial data. This helper should be removed when
    ValidatedSeries becomes the report's historical-data source.
    """
    if not isinstance(table, list):
        return []

    for row in table[1:]:
        if not isinstance(row, list) or not row:
            continue

        if str(row[0]).strip() != metric:
            continue

        values: list[float] = []

        for value in row[1:]:
            if isinstance(value, bool):
                continue

            if isinstance(value, (int, float)):
                values.append(float(value))

        return values

    return []


def _validated_registry(
    validated_metrics: Any,
) -> Any:
    """
    Normalize either a ValidatedMetricRegistry or a metric mapping.

    The report remains compatible with serialized registry dictionaries while
    preferring the canonical registry object attached by the orchestrator.
    """
    if validated_metrics is None:
        return {}

    metrics = getattr(
        validated_metrics,
        "metrics",
        None,
    )

    if metrics is not None:
        return metrics

    return validated_metrics


def _validated_metric_value(
    validated_metrics: Any,
    *metric_names: str,
) -> float | None:
    """
    Return the first report-safe canonical metric value.

    Withheld, partial, unavailable, and unsafe values remain None. Missing
    financial facts are never interpreted as zero.
    """
    registry = _validated_registry(
        validated_metrics
    )

    getter = getattr(
        registry,
        "get",
        None,
    )

    if not callable(getter):
        return None

    for metric_name in metric_names:
        metric = getter(metric_name)

        if metric is None:
            continue

        if isinstance(metric, dict):
            value = metric.get("value")

            safe_for_report = metric.get(
                "is_safe_for_report"
            )

            status = metric.get(
                "validation_status",
                metric.get("status"),
            )

            if hasattr(status, "value"):
                status = status.value
        else:
            value = getattr(
                metric,
                "value",
                None,
            )

            safe_for_report = getattr(
                metric,
                "is_safe_for_report",
                None,
            )

            status = getattr(
                metric,
                "validation_status",
                None,
            )

            if hasattr(status, "value"):
                status = status.value

        normalized_status = str(
            status or ""
        ).strip().lower()

        if safe_for_report is False:
            continue

        if normalized_status in {
            "partial",
            "withheld",
            "unavailable",
            "invalid",
            "failed",
            "unsafe",
        }:
            continue

        if isinstance(value, bool):
            continue

        if isinstance(value, (int, float)):
            return float(value)

    return None



def _growth_rate(
    newest: float | None,
    oldest: float | None,
) -> float | None:
    if newest is None or oldest in {None, 0}:
        return None

    return (newest / oldest - 1) * 100



def _clean_text(
    value: Any,
    default: str,
) -> str:
    text = str(value or "").strip()

    if text in {
        "",
        "N/A",
        "None",
        "Unknown",
    }:
        return default

    return text


def _concise_business_model(
    company_name: str,
    industry: str,
    company_description: str,
) -> str:
    """
    Generate an institutional-quality business model summary instead
    of simply shortening the company description.
    """

    description = _clean_text(
        company_description,
        "",
    ).lower()

    industry_lower = industry.lower()

    biotech = any(
        word in industry_lower or word in description
        for word in (
            "biotech",
            "biotechnology",
            "pharmaceutical",
            "drug",
            "therapeutic",
        )
    )

    platform = any(
        word in description
        for word in (
            "platform",
            "artificial intelligence",
            "machine learning",
            "automation",
            "data science",
        )
    )

    partnerships = any(
        word in description
        for word in (
            "collaboration",
            "partner",
            "licensing",
            "license",
            "milestone",
            "agreement",
        )
    )

    if biotech and platform:

        if partnerships:
            return (
                f"{company_name} operates a platform-based biotechnology "
                "model combining internally developed therapeutic "
                "programs with strategic pharmaceutical partnerships. "
                "Near-term revenue is primarily generated through "
                "research collaborations, licensing, and milestone "
                "agreements, while long-term value depends on successful "
                "clinical development, regulatory approvals, and future "
                "commercialization."
            )

        return (
            f"{company_name} operates a platform-based biotechnology "
            "business focused on converting computational discovery into "
            "clinically validated therapeutic assets. Long-term value "
            "depends on successful clinical execution, regulatory "
            "progress, and commercialization."
        )

    if biotech:
        return (
            f"{company_name} develops therapeutic assets through a "
            "clinical-stage biotechnology model. Value creation depends "
            "on advancing the pipeline through clinical development, "
            "regulatory approval, and eventual commercialization."
        )

    if description:

        sentences = [
            s.strip()
            for s in description.replace(
                "\n",
                " ",
            ).split(".")
            if s.strip()
        ]

        if sentences:
            concise = ". ".join(sentences[:2])

            if len(concise) > 420:
                concise = concise[:417].rsplit(
                    " ",
                    1,
                )[0] + "..."

            return concise.capitalize().rstrip(".") + "."

    return (
        f"{company_name} operates in {industry_lower}, "
        "combining internal operations with commercial and strategic "
        "growth initiatives."
    )


def build_executive_summary(
    company_name: str,
    ticker: str,
    exchange: str,
    industry: str,
    company_description: str,
    income_statement: list[list[Any]],
    balance_sheet: list[list[Any]],
    cash_flow: list[list[Any]],
    estimated_runway: str,
    latest_filing: str,
    validated_metrics: Any = None,
) -> dict[str, Any]:
    revenues = _numeric_statement_series(
        income_statement,
        "Revenue",
    )
    rd_values = _numeric_statement_series(
        income_statement,
        "R&D Expense",
    )

    revenue_growth = (
        _growth_rate(
            revenues[0],
            revenues[-1],
        )
        if revenues[1:]
        else None
    )

    rd_growth = (
        _growth_rate(
            rd_values[0],
            rd_values[-1],
        )
        if rd_values[1:]
        else None
    )

    latest_revenue = (
        revenues[0]
        if revenues
        else None
    )

    latest_rd = (
        rd_values[0]
        if rd_values
        else None
    )

    # Canonical current-state financial facts.
    #
    # Cash and debt are resolved once by the validated financial registry and
    # reused throughout the report. No display-table fallback is permitted.
    cash = _validated_metric_value(
        validated_metrics,
        "cash_and_cash_equivalents",
    )
    debt = _validated_metric_value(
        validated_metrics,
        "financial_debt",
    )

    # Temporary historical-flow compatibility path.
    #
    # These values are accepted only when the normalized statement contains
    # raw numeric observations. No formatted display strings are reparsed.
    # ValidatedSeries will replace this path.
    free_cash_flow_values = _numeric_statement_series(
        cash_flow,
        "Free Cash Flow",
    )
    net_income_values = _numeric_statement_series(
        income_statement,
        "Net Income",
    )

    free_cash_flow = (
        free_cash_flow_values[0]
        if free_cash_flow_values
        else None
    )
    net_income = (
        net_income_values[0]
        if net_income_values
        else None
    )

    assessment = build_financial_assessment(
        revenue_growth=revenue_growth,
        rd_growth=rd_growth,
        latest_revenue=latest_revenue,
        latest_rd=latest_rd,
        cash=cash,
        debt=debt,
        free_cash_flow=free_cash_flow,
        net_income=net_income,
        estimated_runway=estimated_runway,
    )

    financial_points: list[str] = []
    investment_highlights: list[str] = []
    key_risks: list[str] = []
    catalysts: list[str] = []

    cash_interpretation = interpret_cash_position(
        assessment["liquidity"],
        format_money=format_report_money,
    )


    balance_sheet_interpretation = (
        interpret_balance_sheet_position(
            assessment["liquidity"],
            format_money=format_report_money,
        )
    )

    liquidity_parts = [
        item
        for item in (
            cash_interpretation,
            balance_sheet_interpretation,
        )
        if item
    ]

    if liquidity_parts:
        investment_highlights.append(
            " ".join(liquidity_parts)
        )

    revenue_assessment = assessment["revenue"]

    if revenue_assessment["growth_pct"] is not None:
        direction = {
            "increase": "increased",
            "decline": "declined",
            "flat": "was unchanged by",
        }.get(
            revenue_assessment["direction"],
            "changed",
        )

        financial_points.append(
            (
                f"Revenue {direction} approximately "
                f"{revenue_assessment['absolute_growth_pct']:.0f}% "
                "across the available annual periods."
            )
        )

        revenue_interpretation = (
            interpret_revenue_growth(
                revenue_assessment,
                industry=industry,
            )
        )

        if revenue_interpretation:
            investment_highlights.append(
                revenue_interpretation
            )

    if latest_revenue is not None:
        financial_points.append(
            (
                f"Latest reported annual revenue was "
                f"approximately "
                f"{format_report_money(latest_revenue)}."
            )
        )

    research_assessment = assessment[
        "research_investment"
    ]

    if research_assessment["growth_pct"] is not None:
        direction = {
            "increase": "increased",
            "decline": "declined",
            "flat": "was unchanged by",
        }.get(
            research_assessment["direction"],
            "changed",
        )

        financial_points.append(
            (
                f"R&D spending {direction} approximately "
                f"{research_assessment['absolute_growth_pct']:.0f}% "
                "across the available annual periods."
            )
        )

    rd_interpretation = interpret_research_investment(
        research_assessment,
        format_money=format_report_money,
    )

    if rd_interpretation:
        investment_highlights.append(
            rd_interpretation
        )

    profitability_assessment = assessment[
        "profitability"
    ]
    cash_flow_state = profitability_assessment[
        "cash_flow_state"
    ]
    free_cash_flow_magnitude = profitability_assessment[
        "free_cash_flow_magnitude"
    ]

    if cash_flow_state == "cash_burning":
        financial_points.append(
            (
                "Annual free cash flow was negative "
                "at approximately "
                f"{format_report_money(free_cash_flow_magnitude)}."
            )
        )

        cash_burn_risk = interpret_cash_burn_risk(
            profitability_assessment,
            format_money=format_report_money,
        )

        if cash_burn_risk:
            key_risks.append(
                cash_burn_risk
            )

    elif cash_flow_state == "cash_generative":
        financial_points.append(
            (
                "Annual free cash flow was positive "
                "at approximately "
                f"{format_report_money(free_cash_flow_magnitude)}."
            )
        )

    elif cash_flow_state == "neutral":
        financial_points.append(
            "Annual free cash flow was approximately break-even."
        )

    profitability_risk = (
        interpret_profitability_risk(
            profitability_assessment
        )
    )

    if profitability_risk:
        key_risks.append(
            profitability_risk
        )

    balance_sheet_risk = (
        interpret_balance_sheet_risk(
            assessment["liquidity"]
        )
    )

    if balance_sheet_risk:
        key_risks.append(
            balance_sheet_risk
        )

    if assessment["liquidity"]["runway_available"]:
        financial_points.append(
            (
                "Estimated funding runway is "
                f"{assessment['liquidity']['estimated_runway']}."
            )
        )

    industry_lower = industry.lower()

    if any(
        term in industry_lower
        for term in [
            "biotech",
            "biotechnology",
            "pharmaceutical",
            "drug",
            "therapeutic",
        ]
    ):
        key_risks.extend(
            development_risks(
                industry
            )
        )

        catalysts.extend(
            [
                "Clinical data and pipeline-development updates.",
                (
                    "Regulatory, enrollment, or program-"
                    "advancement milestones."
                ),
            ]
        )
    else:
        key_risks.extend(
            development_risks(
                industry
            )
        )

        catalysts.append(
            (
                "Product, platform, or commercial execution "
                "updates."
            )
        )

    catalysts.extend(
        [
            (
                "New strategic partnership or milestone "
                "announcements."
            ),
            (
                "Quarterly financial and liquidity updates."
            ),
        ]
    )

    if latest_filing not in {
        "",
        "N/A",
        "No recent filing available",
    }:
        catalysts.append(
            f"Review of the latest disclosed filing: {latest_filing}."
        )

    default_highlights = [
        (
            "The company operates in a market where technical "
            "execution and differentiated capabilities may "
            "support long-term value creation."
        ),
        (
            "Strategic partnerships may expand development, "
            "validation, or commercialization opportunities."
        ),
        (
            "Successful execution of internal programs could "
            "strengthen the company’s operating position."
        ),
    ]

    for item in default_highlights:
        if len(investment_highlights) >= 4:
            break

        investment_highlights.append(item)

    default_risks = [
        (
            "Failure to convert technical capabilities into "
            "durable commercial revenue remains a central risk."
        ),
        (
            "Competitive pressure may reduce differentiation "
            "or increase required investment."
        ),
        (
            "Future capital needs may result in shareholder "
            "dilution."
        ),
    ]

    for item in default_risks:
        if len(key_risks) >= 4:
            break

        key_risks.append(item)

    business_model = _concise_business_model(
        company_name=company_name,
        industry=industry,
        company_description=company_description,
    )

    company_identity = (
        f"{company_name} "
        f"({exchange}: {ticker})"
        if exchange not in {
            "",
            "N/A",
            "Unknown",
        }
        else f"{company_name} ({ticker})"
    )

    overview = (
        f"{company_identity} operates in {industry}. "
        f"{business_model}"
    )

    # Preserve the legacy keys used by the current PDF
    # renderer while adding the new commercial structure.
    return {
        "title": "Executive Summary",
        "company": company_identity,
        "company_name": company_name,
        "ticker": ticker,
        "exchange": exchange,
        "industry": industry,
        "business_model": business_model,
        "investment_highlights": investment_highlights[:4],
        "key_risks": key_risks[:4],
        "key_catalysts": catalysts[:4],
        "financial_snapshot": {
            "Revenue": format_report_money(
                latest_revenue
            ),
            "Cash": format_report_money(cash),
            "Debt": format_report_money(debt),
            "Net Income": format_report_money(
                net_income
            ),
            "Free Cash Flow": format_report_money(
                free_cash_flow
            ),
            "Estimated Runway": estimated_runway,
            "Indicative Cash Runway": estimated_runway,
        },
        "financial_analysis": " ".join(
            financial_points
        ),
        "latest_filing": latest_filing,
        "overview": overview,
        "bull_case": investment_highlights[:4],
        "bear_case": key_risks[:4],
    }

