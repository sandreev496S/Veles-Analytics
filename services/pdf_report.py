from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


VEL_BLACK = colors.HexColor("#12151A")
VEL_DARK = colors.HexColor("#2B303A")
VEL_PANEL = colors.HexColor("#3E434D")
VEL_BLUE = colors.HexColor("#A1BAC5")
VEL_LINE = colors.HexColor("#555D66")
VEL_LIGHT = colors.HexColor("#F3F6F8")
VEL_TEXT = colors.HexColor("#222222")
WHITE = colors.white


def _header_footer(canvas, doc):
    width, height = LETTER
    canvas.saveState()

    canvas.setFillColor(VEL_BLACK)
    canvas.rect(0, height - 0.75 * inch, width, 0.75 * inch, fill=1, stroke=0)

    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(0.65 * inch, height - 0.45 * inch, "VELES ANALYTICS")

    canvas.setFillColor(VEL_BLUE)
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(width - 0.65 * inch, height - 0.45 * inch, "DCF VALUATION REPORT")

    canvas.setStrokeColor(VEL_LINE)
    canvas.line(0.65 * inch, 0.55 * inch, width - 0.65 * inch, 0.55 * inch)

    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(0.65 * inch, 0.35 * inch, "Veles Analytics | Confidential")
    canvas.drawRightString(width - 0.65 * inch, 0.35 * inch, f"Page {doc.page}")

    canvas.restoreState()


def _section(title, styles):
    return [
        Spacer(1, 0.18 * inch),
        Paragraph(title, styles["SectionTitle"]),
        Spacer(1, 0.06 * inch),
    ]


def _format_value(value):
    try:
        if isinstance(value, float):
            return f"{value:,.2f}"
        if isinstance(value, int):
            return f"{value:,}"
        return str(value)
    except Exception:
        return str(value)


def _df_to_table(df, max_rows=None):
    if max_rows is not None:
        df = df.head(max_rows)

    clean_df = df.copy()

    for col in clean_df.columns:
        clean_df[col] = clean_df[col].apply(_format_value)

    data = [list(clean_df.columns)] + clean_df.values.tolist()

    table = Table(data, repeatRows=1, hAlign="LEFT")

    style = [
        ("GRID", (0, 0), (-1, -1), 0.35, VEL_LINE),
        ("BACKGROUND", (0, 0), (-1, 0), VEL_BLACK),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]

    for row in range(1, len(data)):
        if row % 2 == 0:
            style.append(("BACKGROUND", (0, row), (-1, row), VEL_LIGHT))
        else:
            style.append(("BACKGROUND", (0, row), (-1, row), WHITE))

    table.setStyle(TableStyle(style))
    return table


def _metric_table(metrics):
    data = [["Metric", "Value"]]

    for key, value in metrics.items():
        data.append([key, _format_value(value)])

    table = Table(data, colWidths=[2.8 * inch, 2.4 * inch], hAlign="LEFT")

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.35, VEL_LINE),
        ("BACKGROUND", (0, 0), (-1, 0), VEL_BLACK),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 1), (-1, -1), WHITE),
    ]))

    return table


def create_dcf_pdf(
    company_name,
    summary_df,
    forecast_df,
    sensitivity_df,
    comps_df=None,
    comps_summary_df=None,
    valuation_crosscheck_df=None,
    memo_text=None,
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.95 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=VEL_BLACK,
        spaceAfter=10,
    ))

    styles.add(ParagraphStyle(
        name="Subtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#666666"),
        spaceAfter=12,
    ))

    styles.add(ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=VEL_BLACK,
        spaceBefore=8,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="BodyClean",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=VEL_TEXT,
        spaceAfter=7,
    ))

    styles.add(ParagraphStyle(
        name="MemoHeading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=VEL_BLACK,
        spaceBefore=8,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="MemoBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        textColor=VEL_TEXT,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="MemoBullet",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        leftIndent=14,
        firstLineIndent=-8,
        textColor=VEL_TEXT,
        spaceAfter=5,
    ))

    story = []

    story.append(Paragraph(f"{company_name} DCF Valuation Report", styles["ReportTitle"]))
    story.append(Paragraph("Generated by Veles DCF Analyst | Professional valuation output", styles["Subtitle"]))
    story.append(Spacer(1, 0.10 * inch))

    story.extend(_section("Executive Summary", styles))

    base_row = summary_df[summary_df["Scenario"] == "Base Case"]

    if not base_row.empty:
        base = base_row.iloc[0]
        metrics = {
            "Base Case Enterprise Value ($M)": base.get("Enterprise Value ($M)", ""),
            "Base Case Equity Value ($M)": base.get("Equity Value ($M)", ""),
            "Base Case Implied Share Price ($)": base.get("Implied Share Price ($)", ""),
            "Base Case Margin of Safety Price ($)": base.get("MoS Price ($)", ""),
            "Terminal Value Contribution": f"{base.get('Terminal Value %', 0):.2%}",
        }
        story.append(_metric_table(metrics))
        story.append(Spacer(1, 0.15 * inch))

    story.extend(_section("Scenario Valuation Summary", styles))
    story.append(_df_to_table(summary_df))
    story.append(Spacer(1, 0.15 * inch))

    story.extend(_section("Base Case Forecast", styles))
    story.append(_df_to_table(forecast_df))
    story.append(Spacer(1, 0.15 * inch))

    story.extend(_section("Sensitivity Matrix", styles))
    sensitivity_display = sensitivity_df.reset_index().rename(columns={"index": "Discount Rate"})
    story.append(_df_to_table(sensitivity_display))
    story.append(Spacer(1, 0.15 * inch))

    if comps_df is not None and not comps_df.empty:
        story.extend(_section("Comparable Company Analysis", styles))

        story.append(
            Paragraph(
                "<b>Methodology:</b> Core Operating Peers are used to "
                "determine the primary trading-comps medians. Nuclear "
                "Reference Peers provide sector context but are excluded "
                "from the core median. The target company is shown only "
                "for comparison and is also excluded from peer medians.",
                styles["BodyText"],
            )
        )
        story.append(Spacer(1, 0.08 * inch))

        comp_cols = [
            "Company",
            "Ticker",
            "Peer Type",
            "Revenue Growth",
            "EBITDA Margin",
            "EV/Revenue",
            "EV/EBITDA",
            "P/E",
        ]

        comp_cols = [
            c for c in comp_cols
            if c in comps_df.columns
        ]

        pdf_comps = comps_df[comp_cols].copy()

        # Report-facing peer taxonomy. This changes presentation only;
        # the underlying peer selection and valuation calculations remain
        # untouched.
        if "Peer Type" in pdf_comps.columns:
            def _report_peer_group(value):
                value = str(value or "")

                if value == "Target Company":
                    return "Target Company"

                if value.startswith("Direct /"):
                    return "Core Operating Peer"

                return "Strategic / Nuclear Reference"

            pdf_comps["Peer Type"] = (
                pdf_comps["Peer Type"].map(_report_peer_group)
            )

        def _pdf_pct(value):
            try:
                value = float(value)
                if value != value:
                    return "—"
                return f"{value:.1%}"
            except (TypeError, ValueError):
                return "—"

        def _pdf_multiple(value):
            try:
                value = float(value)
                if value != value:
                    return "—"
                return f"{value:.2f}x"
            except (TypeError, ValueError):
                return "—"

        if "Revenue Growth" in pdf_comps.columns:
            pdf_comps["Revenue Growth"] = (
                pdf_comps["Revenue Growth"].map(_pdf_pct)
            )

        if "EBITDA Margin" in pdf_comps.columns:
            pdf_comps["EBITDA Margin"] = (
                pdf_comps["EBITDA Margin"].map(_pdf_pct)
            )

        for multiple_col in [
            "EV/Revenue",
            "EV/EBITDA",
            "P/E",
        ]:
            if multiple_col in pdf_comps.columns:
                pdf_comps[multiple_col] = (
                    pdf_comps[multiple_col].map(_pdf_multiple)
                )

        pdf_comps = pdf_comps.rename(
            columns={
                "Revenue Growth": "Growth",
                "EBITDA Margin": "EBITDA Margin",
            }
        )

        story.append(_df_to_table(pdf_comps))
        story.append(Spacer(1, 0.12 * inch))

    # ----------------------------------------------------------
    # COMPARABLE VALUATION + CROSS-CHECK
    #
    # Render side-by-side to keep the complete valuation section
    # together on page 2 and avoid an almost-empty third page.
    # ----------------------------------------------------------
    summary_table = None
    crosscheck_table = None

    if comps_summary_df is not None and not comps_summary_df.empty:
        summary_keep = [
            "Median EV/Revenue",
            "Median EV/EBITDA",
            "Median P/E",
            "Implied Share Price from Revenue ($)",
            "Implied Share Price from EBITDA ($)",
            "Implied Share Price from P/E ($)",
        ]

        compact_summary = comps_summary_df[
            comps_summary_df["Metric"].isin(summary_keep)
        ].copy()

        def _summary_value(row):
            metric = str(row["Metric"])
            value = row["Value"]

            try:
                value = float(value)
            except (TypeError, ValueError):
                return "—"

            if value != value:
                return "—"

            if metric.startswith("Median"):
                return f"{value:.2f}x"

            if "Share Price" in metric:
                return f"${value:.2f}"

            return f"{value:,.2f}"

        compact_summary["Value"] = compact_summary.apply(
            _summary_value,
            axis=1,
        )

        # Shorter labels make the left-hand box substantially cleaner.
        compact_summary["Metric"] = compact_summary["Metric"].replace({
            "Median EV/Revenue": "Median EV / Revenue",
            "Median EV/EBITDA": "Median EV / EBITDA",
            "Median P/E": "Median P / E",
            "Implied Share Price from Revenue ($)": "EV / Revenue Price",
            "Implied Share Price from EBITDA ($)": "EV / EBITDA Price",
            "Implied Share Price from P/E ($)": "P / E Price",
        })

        summary_table = _df_to_table(compact_summary)

    if (
        valuation_crosscheck_df is not None
        and not valuation_crosscheck_df.empty
    ):
        crosscheck_pdf = valuation_crosscheck_df.copy()

        if "Implied Share Price ($)" in crosscheck_pdf.columns:
            crosscheck_pdf["Implied Share Price ($)"] = (
                crosscheck_pdf["Implied Share Price ($)"]
                .map(
                    lambda x: (
                        f"${float(x):.2f}"
                        if x is not None and float(x) == float(x)
                        else "—"
                    )
                )
            )

        crosscheck_pdf = crosscheck_pdf.rename(
            columns={
                "Implied Share Price ($)": "Price",
            }
        )

        crosscheck_pdf["Methodology"] = (
            crosscheck_pdf["Methodology"]
            .replace({
                "DCF — Base Case": "DCF — Base",
                "Trading Comps — EV / Revenue": "Comps — EV / Revenue",
                "Trading Comps — EV / EBITDA": "Comps — EV / EBITDA",
                "Trading Comps — P / E": "Comps — P / E",
            })
        )

        crosscheck_table = _df_to_table(crosscheck_pdf)

    if summary_table is not None or crosscheck_table is not None:
        left_story = []
        right_story = []

        if summary_table is not None:
            left_story.append(
                Paragraph(
                    "<b>Comparable Valuation Summary</b>",
                    styles["Heading2"],
                )
            )
            left_story.append(Spacer(1, 0.06 * inch))
            left_story.append(summary_table)

        if crosscheck_table is not None:
            right_story.append(
                Paragraph(
                    "<b>Valuation Cross-Check</b>",
                    styles["Heading2"],
                )
            )
            right_story.append(Spacer(1, 0.06 * inch))
            right_story.append(crosscheck_table)

        valuation_grid = Table(
            [[left_story, right_story]],
            colWidths=[3.35 * inch, 3.35 * inch],
            hAlign="LEFT",
        )

        valuation_grid.setStyle(
            TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (0, 0), 0),
                ("RIGHTPADDING", (0, 0), (0, 0), 10),
                ("LEFTPADDING", (1, 0), (1, 0), 10),
                ("RIGHTPADDING", (1, 0), (1, 0), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ])
        )

        story.append(Spacer(1, 0.08 * inch))
        story.append(valuation_grid)
        story.append(Spacer(1, 0.15 * inch))

    if memo_text:
        story.append(PageBreak())
        story.extend(_section("AI Investment Memo", styles))

        for paragraph in memo_text.split("\n"):
            cleaned = paragraph.strip()

            if not cleaned:
                story.append(Spacer(1, 0.06 * inch))
                continue

            cleaned = (
                cleaned
                .replace("**", "")
                .replace("###", "")
                .replace("##", "")
                .replace("#", "")
            ).strip()

            if cleaned[:2].isdigit() and "." in cleaned[:4]:
                story.append(Spacer(1, 0.10 * inch))
                story.append(Paragraph(cleaned, styles["MemoHeading"]))
                story.append(Spacer(1, 0.04 * inch))

            elif cleaned.startswith("- "):
                bullet_text = cleaned[2:].strip()
                story.append(Paragraph(f"• {bullet_text}", styles["MemoBullet"]))

            else:
                story.append(Paragraph(cleaned, styles["MemoBody"]))

    doc.build(
        story,
        onFirstPage=_header_footer,
        onLaterPages=_header_footer,
    )

    pdf = buffer.getvalue()
    buffer.close()

    return pdf


def create_rnpv_pdf(
    asset_name,
    valuation_df,
    forecast_df,
    clinical_stage=None,
    memo_text=None,
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.95 * inch,
        bottomMargin=0.75 * inch,
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="RNPVTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=26,
        textColor=VEL_BLACK,
        spaceAfter=10,
    ))

    styles.add(ParagraphStyle(
        name="RNPVSubtitle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#666666"),
        spaceAfter=12,
    ))

    styles.add(ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=VEL_BLACK,
        spaceBefore=8,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="BodyClean",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=VEL_TEXT,
        spaceAfter=7,
    ))

    styles.add(ParagraphStyle(
        name="MemoHeading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=VEL_BLACK,
        spaceBefore=8,
        spaceAfter=4,
    ))

    styles.add(ParagraphStyle(
        name="MemoBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        textColor=VEL_TEXT,
        spaceAfter=6,
    ))

    styles.add(ParagraphStyle(
        name="MemoBullet",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        leftIndent=14,
        firstLineIndent=-8,
        textColor=VEL_TEXT,
        spaceAfter=5,
    ))

    story = []

    story.append(Paragraph(f"{asset_name} Biotech rNPV Report", styles["RNPVTitle"]))
    story.append(Paragraph("Generated by Veles DCF Analyst | Probability-adjusted biotech valuation", styles["RNPVSubtitle"]))

    if clinical_stage:
        story.append(Paragraph(f"Clinical / Regulatory Stage: {clinical_stage}", styles["RNPVSubtitle"]))

    story.append(Spacer(1, 0.12 * inch))

    story.extend(_section("rNPV Valuation Summary", styles))
    story.append(_df_to_table(valuation_df))
    story.append(Spacer(1, 0.15 * inch))

    story.extend(_section("Probability-Adjusted Forecast", styles))
    story.append(_df_to_table(forecast_df))
    story.append(Spacer(1, 0.15 * inch))

    if memo_text:
        story.append(PageBreak())
        story.extend(_section("AI Biotech Valuation Memo", styles))

        for paragraph in memo_text.split("\n"):
            cleaned = paragraph.strip()

            if not cleaned:
                story.append(Spacer(1, 0.06 * inch))
                continue

            cleaned = (
                cleaned
                .replace("**", "")
                .replace("###", "")
                .replace("##", "")
                .replace("#", "")
            ).strip()

            if cleaned[:2].isdigit() and "." in cleaned[:4]:
                story.append(Spacer(1, 0.10 * inch))
                story.append(Paragraph(cleaned, styles["MemoHeading"]))
                story.append(Spacer(1, 0.04 * inch))

            elif cleaned.startswith("- "):
                bullet_text = cleaned[2:].strip()
                story.append(Paragraph(f"• {bullet_text}", styles["MemoBullet"]))

            else:
                story.append(Paragraph(cleaned, styles["MemoBody"]))

    doc.build(
        story,
        onFirstPage=_header_footer,
        onLaterPages=_header_footer,
    )

    pdf = buffer.getvalue()
    buffer.close()

    return pdf
