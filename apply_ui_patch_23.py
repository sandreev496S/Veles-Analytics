from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title(
        "Research Modules",
        "The company workspace will eventually replace scattered pages."
    )'''

new = '''    section_title(
        "Research Modules",
        "Company profile, funding, technology, competition, valuation history, notes, and reports."
    )'''

if old not in text:
    raise SystemExit("Could not find Research Modules title block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 23 applied: Research Modules subtitle improved.")
