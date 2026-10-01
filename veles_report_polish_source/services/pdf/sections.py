from __future__ import annotations

import re
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from services.pdf.theme import PDFTheme, VELES_PDF_THEME


def slugify_anchor(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return slug.strip("_") or "section"


def anchored_heading(
    title: str,
    styles: dict,
    *,
    level: int = 0,
    anchor: str | None = None,
    style_name: str = "h1",
):
    anchor = anchor or slugify_anchor(title)

    paragraph = Paragraph(
        f'<a name="{escape(anchor)}"/>{escape(str(title))}',
        styles[style_name],
    )

    paragraph._veles_toc_level = level
    paragraph._veles_toc_title = str(title)
    paragraph._veles_anchor = anchor

    return paragraph


def section_heading(
    title: str,
    styles: dict,
    *,
    anchor: str | None = None,
):
    return anchored_heading(
        title,
        styles,
        level=0,
        anchor=anchor,
        style_name="h1",
    )


def subsection_heading(
    title: str,
    styles: dict,
    *,
    anchor: str | None = None,
):
    return anchored_heading(
        title,
        styles,
        level=1,
        anchor=anchor,
        style_name="h2",
    )


def section_header_bar(
    title: str,
    styles: dict,
    *,
    subtitle: str = "",
    anchor: str | None = None,
    toc_level: int = 0,
    theme: PDFTheme = VELES_PDF_THEME,
):
    anchor = anchor or slugify_anchor(title)

    heading = anchored_heading(
        title,
        styles,
        level=toc_level,
        anchor=anchor,
        style_name="dashboard_subheading",
    )

    content = [heading]

    if subtitle:
        subtitle_style = styles["small"].clone(
            f"{anchor}_subtitle"
        )
        subtitle_style.textColor = colors.HexColor("#E2E8F0")

        content.append(
            Paragraph(
                escape(str(subtitle)),
                subtitle_style,
            )
        )

    table = Table(
        [[content]],
        colWidths=[theme.content_width],
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), theme.primary),
                ("LEFTPADDING", (0, 0), (-1, -1), 11),
                ("RIGHTPADDING", (0, 0), (-1, -1), 11),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    # The document only sees top-level flowables. Register the outer
    # component so it appears in the automatic TOC.
    table._veles_toc_level = toc_level
    table._veles_toc_title = str(title)
    table._veles_anchor = anchor

    return KeepTogether(
        [
            table,
            Spacer(1, theme.section_gap),
        ]
    )


def cross_reference(
    label: str,
    anchor: str,
    styles: dict,
):
    return Paragraph(
        f'<a href="#{escape(anchor)}">{escape(label)}</a>',
        styles["body"],
    )


def narrative_section(
    heading: str,
    body: str,
    styles: dict,
    *,
    use_bar: bool = True,
    anchor: str | None = None,
    subtitle: str = "",
    theme: PDFTheme = VELES_PDF_THEME,
):
    safe_body = escape(str(body)).replace("\n", "<br/>")

    heading_component = (
        section_header_bar(
            heading,
            styles,
            subtitle=subtitle,
            anchor=anchor,
            theme=theme,
        )
        if use_bar
        else section_heading(
            heading,
            styles,
            anchor=anchor,
        )
    )

    return [
        heading_component,
        Paragraph(
            safe_body,
            styles["body"],
        ),
        Spacer(1, theme.paragraph_gap),
    ]
