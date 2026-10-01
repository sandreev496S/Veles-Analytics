from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with col3:
        metric_card("Coverage", "5", "Tracked Companies")'''

new = '''    tracked_companies_count = 5

    with col3:
        metric_card("Coverage", tracked_companies_count, "Tracked Companies")'''

if old not in text:
    raise SystemExit("Could not find Coverage KPI block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 35 applied: Coverage KPI now uses a variable.")
