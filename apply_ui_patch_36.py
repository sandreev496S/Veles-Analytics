from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title(
        "Platform Overview",
        "Your research, valuation, and report-generation command center."
    )

    col1, col2, col3, col4 = st.columns(4)'''

new = '''    section_title(
        "Platform Overview",
        "Your research, valuation, and report-generation command center."
    )

    tracked_companies = [
        "Neuralink",
        "Synchron",
        "Paradromics",
        "Blackrock Neurotech",
        "Precision Neuroscience",
    ]

    col1, col2, col3, col4 = st.columns(4)'''

if old not in text:
    raise SystemExit("Could not find Platform Overview block.")

text = text.replace(old, new, 1)

old2 = '''    tracked_companies_count = 5

    with col3:
        metric_card("Coverage", tracked_companies_count, "Tracked Companies")'''

new2 = '''    with col3:
        metric_card("Coverage", len(tracked_companies), "Tracked Companies")'''

if old2 not in text:
    raise SystemExit("Could not find tracked_companies_count block.")

text = text.replace(old2, new2, 1)

path.write_text(text)
print("UI patch 36 applied: Dashboard tracked companies centralized.")
