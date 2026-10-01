from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title(
        "Operating Metrics",
        "Current platform coverage, saved models, report output, and system readiness."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Valuations", valuations_count, "Saved Models")

    with col2:
        metric_card("Reports", reports_count, "Cloud Reports")

    with col3:
        metric_card("Coverage", len(tracked_companies.keys()), "Tracked Companies")

    with col4:
        metric_card("Platform", "Online", "System Ready")

'''

if old not in text:
    raise SystemExit("Could not find duplicate Operating Metrics block.")

text = text.replace(old, "", 1)
path.write_text(text)

print("Removed duplicate Operating Metrics counter section.")
