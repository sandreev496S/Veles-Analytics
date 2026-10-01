from __future__ import annotations

from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from services.pdf.callouts import analyst_callout
from services.pdf.sections import section_header_bar
from services.pdf.tables import build_table
from services.pdf.theme import PDFTheme, VELES_PDF_THEME


def _summary_cards(
    summary: dict,
    styles: dict,
    theme: PDFTheme,
):
    metrics = [
        (
            "Implied Value / Share",
            summary.get(
                "implied_value_per_share",
                "N/A",
            ),
        ),
        (
            "Current Share Price",
            summary.get(
                "current_share_price",
                "N/A",
            ),
        ),
        (
            "Implied Upside / Downside",
            summary.get(
                "implied_upside",
                "N/A",
            ),
        ),
        (
            "WACC",
            summary.get("wacc", "N/A"),
        ),
        (
            "Enterprise Value",
            summary.get(
                "enterprise_value",
                "N/A",
            ),
        ),
        (
            "Equity Value",
            summary.get(
                "equity_value",
                "N/A",
            ),
        ),
    ]

    cards = []

    for label, value in metrics:
        content = [
            Paragraph(
                label,
                styles["card_label"],
            ),
            Paragraph(
                str(value),
                styles["card_value"],
            ),
        ]

        card = Table(
            [[content]],
            colWidths=[2.15 * inch],
            rowHeights=[0.72 * inch],
        )

        card.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    theme.card_background,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    theme.border,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ])
        )

        cards.append(card)

    return Table(
        [
            cards[:3],
            cards[3:],
        ],
        colWidths=[2.35 * inch] * 3,
        hAlign="LEFT",
        style=TableStyle([
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP",
            ),
            (
                "LEFTPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),
            (
                "RIGHTPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                3,
            ),
        ]),
    )


def _scenario_table_component(
    data: list[list],
    styles: dict,
    *,
    theme: PDFTheme,
):
    if not data:
        return Spacer(1, 1)

    table_data = []

    for row_index, row in enumerate(data):
        formatted_row = []

        for cell_index, value in enumerate(row):
            style = (
                styles["table_header"]
                if row_index == 0
                else styles["table_cell"]
            )

            formatted_row.append(
                Paragraph(
                    str(value),
                    style,
                )
            )

        table_data.append(formatted_row)

    table = Table(
        table_data,
        colWidths=[
            1.20 * inch,
            1.75 * inch,
            1.75 * inch,
            2.00 * inch,
        ],
        repeatRows=1,
        hAlign="LEFT",
    )

    table_style = [
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            theme.primary,
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white,
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.35,
            theme.light_border,
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE",
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
    ]

    semantic_backgrounds = {
        "Bull": colors.HexColor("#EAF5ED"),
        "Base": colors.HexColor("#EAF0F8"),
        "Bear": colors.HexColor("#F8EDED"),
    }

    semantic_text = {
        "Bull": colors.HexColor("#1F6B3A"),
        "Base": theme.primary,
        "Bear": colors.HexColor("#8B2C2C"),
    }

    for row_index, row in enumerate(
        data[1:],
        start=1,
    ):
        scenario_name = str(row[0])

        background = semantic_backgrounds.get(
            scenario_name,
            colors.white,
        )
        text_color = semantic_text.get(
            scenario_name,
            theme.body_text,
        )

        table_style.extend([
            (
                "BACKGROUND",
                (0, row_index),
                (-1, row_index),
                background,
            ),
            (
                "TEXTCOLOR",
                (0, row_index),
                (0, row_index),
                text_color,
            ),
            (
                "FONTNAME",
                (0, row_index),
                (0, row_index),
                "Helvetica-Bold",
            ),
        ])

    table.setStyle(
        TableStyle(table_style)
    )

    return table


def _forecast_table_component(
    data: list[list],
    styles: dict,
    *,
    theme: PDFTheme,
):
    if not data:
        return Spacer(1, 1)

    formatted_data = []

    for row_index, row in enumerate(data):
        formatted_row = []

        for value in row:
            style = (
                styles["table_header"]
                if row_index == 0
                else styles["table_cell_compact"]
            )

            formatted_row.append(
                Paragraph(
                    str(value),
                    style,
                )
            )

        formatted_data.append(formatted_row)

    table = Table(
        formatted_data,
        colWidths=[
            0.55 * inch,
            1.10 * inch,
            0.75 * inch,
            0.85 * inch,
            1.05 * inch,
            1.10 * inch,
            1.10 * inch,
        ],
        repeatRows=1,
        hAlign="LEFT",
    )

    table_style = [
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            theme.primary,
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white,
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.3,
            theme.light_border,
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE",
        ),
        (
            "ALIGN",
            (1, 1),
            (-1, -1),
            "RIGHT",
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            4,
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            4,
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            4,
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            4,
        ),
    ]

    first_positive_ebit_row = None

    for row_index, row in enumerate(
        data[1:],
        start=1,
    ):
        background = (
            colors.white
            if row_index % 2 == 1
            else theme.light_background
        )

        table_style.append(
            (
                "BACKGROUND",
                (0, row_index),
                (-1, row_index),
                background,
            )
        )

        # EBIT is column 4 in the formatted report table.
        ebit_text = str(row[4])

        if (
            first_positive_ebit_row is None
            and "$-" not in ebit_text
            and ebit_text not in {
                "N/A",
                "$0.00",
                "$0.00M",
            }
        ):
            first_positive_ebit_row = row_index

    if first_positive_ebit_row is not None:
        table_style.extend([
            (
                "BACKGROUND",
                (0, first_positive_ebit_row),
                (-1, first_positive_ebit_row),
                colors.HexColor("#EAF5ED"),
            ),
            (
                "LINEABOVE",
                (0, first_positive_ebit_row),
                (-1, first_positive_ebit_row),
                0.8,
                theme.positive,
            ),
            (
                "LINEBELOW",
                (0, first_positive_ebit_row),
                (-1, first_positive_ebit_row),
                0.8,
                theme.positive,
            ),
            (
                "FONTNAME",
                (0, first_positive_ebit_row),
                (0, first_positive_ebit_row),
                "Helvetica-Bold",
            ),
        ])

    table.setStyle(
        TableStyle(table_style)
    )

    return table


def _review_flags_component(
    review_flags: list[dict],
    styles: dict,
    *,
    theme: PDFTheme,
):
    if not review_flags:
        return Spacer(1, 1)

    data = [
        [
            Paragraph(
                "Status",
                styles["table_header"],
            ),
            Paragraph(
                "Analyst Review Item",
                styles["table_header"],
            ),
        ]
    ]

    for flag in review_flags:
        data.append([
            Paragraph(
                str(flag.get("status", "Review")),
                styles["table_cell"],
            ),
            Paragraph(
                str(flag.get("item", "")),
                styles["table_cell"],
            ),
        ])

    table = Table(
        data,
        colWidths=[
            1.0 * inch,
            theme.content_width - 1.0 * inch,
        ],
        repeatRows=1,
        hAlign="LEFT",
    )

    table_style = [
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            theme.primary,
        ),
        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white,
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.35,
            theme.light_border,
        ),
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "TOP",
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
    ]

    for row_index, flag in enumerate(
        review_flags,
        start=1,
    ):
        tone = flag.get("tone")

        if tone == "positive":
            background = colors.HexColor("#EAF5ED")
            text_color = colors.HexColor("#1F6B3A")
        else:
            background = colors.HexColor("#FFF7E6")
            text_color = colors.HexColor("#7A4B00")

        table_style.extend([
            (
                "BACKGROUND",
                (0, row_index),
                (-1, row_index),
                background,
            ),
            (
                "TEXTCOLOR",
                (0, row_index),
                (0, row_index),
                text_color,
            ),
            (
                "FONTNAME",
                (0, row_index),
                (0, row_index),
                "Helvetica-Bold",
            ),
        ])

    table.setStyle(
        TableStyle(table_style)
    )

    return table


def build_valuation_section(
    report: dict,
    styles: dict,
    *,
    theme: PDFTheme = VELES_PDF_THEME,
) -> list:
    valuation = report.get("valuation", {})

    if valuation.get("status") != "available":
        return []

    elements: list = [PageBreak()]

    elements.append(
        section_header_bar(
            "DCF Valuation",
            styles,
            subtitle=(
                "Enterprise valuation based on analyst-edited "
                "forecast and capital-market assumptions"
            ),
            anchor="dcf_valuation",
            toc_level=0,
            theme=theme,
        )
    )

    model_status = valuation.get(
        "model_status",
        "illustrative",
    )
    model_note = valuation.get(
        "model_note",
        (
            "Illustrative analytical scenario. "
            "Not a final investment valuation."
        ),
    )
    forecast_years = valuation.get(
        "forecast_years",
        "N/A",
    )

    elements.append(
        Paragraph(
            (
                f"<b>Method:</b> "
                f"{valuation.get('method', 'Enterprise DCF')}<br/>"
                f"<b>Model:</b> "
                f"{valuation.get('name', 'Saved valuation')}<br/>"
                f"<b>Forecast horizon:</b> "
                f"{forecast_years} years<br/>"
                f"<b>Model status:</b> "
                f"{str(model_status).title()}<br/>"
                f"<b>Assumption source:</b> "
                f"{valuation.get('assumption_source', 'Analyst assumptions')}"
            ),
            styles["body"],
        )
    )

    elements.append(
        analyst_callout(
            "Illustrative Valuation Notice",
            model_note,
            styles,
            callout_type="warning",
            width=theme.content_width,
            theme=theme,
        )
    )

    elements.append(Spacer(1, 0.14 * inch))

    elements.append(
        _summary_cards(
            valuation.get("summary", {}),
            styles,
            theme,
        )
    )

    elements.append(Spacer(1, 0.18 * inch))

    elements.append(
        Paragraph(
            "Scenario Analysis",
            styles["h2"],
        )
    )

    elements.append(
        _scenario_table_component(
            valuation.get(
                "scenario_table",
                [],
            ),
            styles,
            theme=theme,
        )
    )

    elements.append(PageBreak())

    elements.append(
        section_header_bar(
            "DCF Forecast",
            styles,
            subtitle=(
                f"{valuation.get('forecast_years', 'Multi')}-year "
                "operating forecast and discounted unlevered free cash flow"
            ),
            anchor="dcf_forecast",
            toc_level=0,
            theme=theme,
        )
    )

    elements.append(
        _forecast_table_component(
            valuation.get(
                "forecast_table",
                [],
            ),
            styles,
            theme=theme,
        )
    )

    sensitivity = valuation.get(
        "sensitivity_table",
        [],
    )

    if sensitivity:
        elements.append(Spacer(1, 0.20 * inch))
        elements.append(
            Paragraph(
                "WACC / Terminal Growth Sensitivity",
                styles["h2"],
            )
        )

        column_count = len(sensitivity[0])
        first_width = 1.35 * inch
        remaining_width = (
            theme.content_width - first_width
        ) / max(column_count - 1, 1)

        elements.append(
            build_table(
                sensitivity,
                col_widths=[
                    first_width,
                    *[
                        remaining_width
                        for _ in range(
                            column_count - 1
                        )
                    ],
                ],
                numeric_columns=set(
                    range(1, column_count)
                ),
                first_column_bold=True,
                compact=True,
                theme=theme,
            )
        )

    elements.append(PageBreak())

    elements.append(
        section_header_bar(
            "DCF Assumptions and Limitations",
            styles,
            subtitle=(
                "Observed inputs, analyst assumptions, "
                "and model-specific cautions"
            ),
            anchor="dcf_assumptions",
            toc_level=0,
            theme=theme,
        )
    )

    elements.append(
        build_table(
            valuation.get("assumption_table", []),
            col_widths=[
                2.15 * inch,
                1.55 * inch,
                3.50 * inch,
            ],
            first_column_bold=True,
            theme=theme,
        )
    )

    review_flags = valuation.get(
        "review_flags",
        [],
    )

    if review_flags:
        elements.append(
            Spacer(
                1,
                0.16 * inch,
            )
        )

        elements.append(
            Paragraph(
                "Analyst Review Flags",
                styles["h2"],
            )
        )

        elements.append(
            _review_flags_component(
                review_flags,
                styles,
                theme=theme,
            )
        )

    return elements
