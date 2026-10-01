from __future__ import annotations

from typing import Any

from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from services.pdf.cards import key_value_panel, metric_card
from services.pdf.sections import section_header_bar
from services.pdf.theme import PDFTheme, VELES_PDF_THEME


def build_dashboard_v2(
    report: dict[str, Any],
    styles: dict,
    *,
    theme: PDFTheme = VELES_PDF_THEME,
) -> list:
    elements: list = []

    elements.append(
        section_header_bar(
            "Executive Dashboard",
            styles,
            subtitle=(
                "Financial position, trading profile, liquidity, "
                "and current research indicators"
            ),
            anchor="executive_dashboard",
            theme=theme,
        )
    )

    elements.append(
        Paragraph(
            (
                f"{report['company_name']} ({report['ticker']}) | "
                f"{report['industry']} | As of {report['date']}"
            ),
            styles["subtitle"],
        )
    )

    metrics = report.get("dashboard_metrics", [])

    for index in range(0, len(metrics), 4):
        group = metrics[index:index + 4]

        while len(group) < 4:
            group.append({
                "label": "",
                "value": "",
                "note": "",
            })

        cards = [
            metric_card(
                metric,
                styles,
                width=1.62 * inch,
                height=0.82 * inch,
                theme=theme,
            )
            for metric in group
        ]

        row = Table(
            [cards],
            colWidths=[1.78 * inch] * 4,
        )

        row.setStyle(
            TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 2),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ]
            )
        )

        elements.append(row)

    elements.append(Spacer(1, 0.16 * inch))

    business_profile = report.get("dashboard_business", {})
    investment_snapshot = report.get("dashboard_investment", {})

    bottom = Table(
        [[
            key_value_panel(
                "Business Profile",
                business_profile,
                styles,
                label_width=1.25 * inch,
                value_width=2.15 * inch,
                theme=theme,
            ),
            key_value_panel(
                "Investment Snapshot",
                investment_snapshot,
                styles,
                label_width=1.25 * inch,
                value_width=2.15 * inch,
                theme=theme,
            ),
        ]],
        colWidths=[
            3.55 * inch,
            3.55 * inch,
        ],
    )

    bottom.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )

    elements.append(bottom)

    return elements
