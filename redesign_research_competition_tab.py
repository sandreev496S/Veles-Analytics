from pathlib import Path

path = Path("app.py")
text = path.read_text()

# Add institutional header immediately after competition tab opens.
old = '''    with competition_tab:
        competition_rows = []'''

new = '''    with competition_tab:
        section_title(
            "Competitive Landscape",
            "Peer universe, differentiation analysis, and strategic positioning."
        )

        competition_rows = []'''

if old not in text:
    raise SystemExit("Could not find competition tab opening block.")

text = text.replace(old, new, 1)

# Rename metric cards.
text = text.replace(
    'metric_card("Peer Companies", len(competition_df), "Tracked Universe")',
    'metric_card("Coverage Universe", len(competition_df), "Tracked Peers")',
    1,
)

text = text.replace(
    'metric_card("Invasive BCIs", invasive_count, "Peer Mix")',
    'metric_card("Invasive Platforms", invasive_count, "Peer Mix")',
    1,
)

text = text.replace(
    'metric_card("Minimally Invasive", minimally_invasive_count, "Peer Mix")',
    'metric_card("Minimally Invasive", minimally_invasive_count, "Platforms")',
    1,
)

# Rename Differentiation Matrix section.
text = text.replace(
'''        section_title(
            "Differentiation Matrix",
            "Early qualitative comparison across technical and commercial dimensions."
        )''',
'''        section_title(
            "Competitive Positioning",
            "Technical, clinical, commercial, and capitalization differentiation."
        )''',
1,
)

# Rename Competitive Scoring Model section.
text = text.replace(
'''        section_title(
            "Competitive Scoring Model",
            "Early qualitative scorecard for market and technology positioning."
        )''',
'''        section_title(
            "Competitive Scorecard",
            "Relative positioning across technology, clinical maturity, capitalization, and regulatory risk."
        )''',
1,
)

# Improve closing activity item label.
text = text.replace(
'''        activity_item(
            "Competitive Angle",
            "This scorecard is a first-pass qualitative model. Next step: replace static scores with analyst inputs and stored company-level research data.",
            "Analysis"
        )''',
'''        activity_item(
            "Strategic Takeaway",
            "This scorecard is a first-pass qualitative model. Next step: replace static scores with analyst inputs, saved diligence notes, and stored company-level research data.",
            "Competitive Intelligence"
        )''',
1,
)

path.write_text(text)

print("Research Workspace competition tab redesigned.")
