from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        "Dashboard",
        "Research Workspace",
        "Standard DCF",'''

new = '''        "Dashboard",
        "Companies",
        "Research Workspace",
        "Standard DCF",'''

if old not in text:
    raise SystemExit("Could not find sidebar nav insertion point.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Companies page added to navigation.")
