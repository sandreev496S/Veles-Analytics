from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Valuations", valuations_count, "Stored")

    with col2:
        metric_card("Reports", reports_count, "Generated")

    with col3:
        metric_card("Coverage", "5", "Neurotech")

    with col4:
        metric_card("Platform", "Online", "Healthy")

    section_title("AI Research Brief", "High-level platform intelligence and market context.")'''

new = '''    section_title(
        "Platform Overview",
        "Your research, valuation, and report-generation command center."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Valuations", valuations_count, "Saved Models")

    with col2:
        metric_card("Reports", reports_count, "Cloud Reports")

    with col3:
        metric_card("Coverage", "5", "Tracked Companies")

    with col4:
        metric_card("Platform", "Online", "System Ready")

    section_title("AI Research Brief", "High-level platform intelligence and market context.")'''

if old not in text:
    raise SystemExit("Could not find KPI dashboard block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 17 applied: KPI row strengthened.")
