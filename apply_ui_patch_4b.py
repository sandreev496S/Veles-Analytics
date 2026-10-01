from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''from styles import (
    load_veles_design_system,
    page_header,
    metric_card,
    insight_card,
    company_card,
)'''

new = '''from styles import (
    load_veles_design_system,
    page_header,
    metric_card,
    insight_card,
    company_card,
    section_title,
    activity_item,
    status_pill,
)'''

if old not in text:
    raise SystemExit("Could not find styles import block in app.py.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 4b applied successfully: new UI components imported.")
