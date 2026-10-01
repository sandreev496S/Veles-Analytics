from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    activity_item,
    status_pill,
)'''

new = '''    activity_item,
    status_pill,
    ai_workflow_card,
)'''

if old not in text:
    raise SystemExit("Could not find import insertion point.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 14b applied successfully: ai_workflow_card imported.")
