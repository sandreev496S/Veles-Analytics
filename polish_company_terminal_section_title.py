from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title(
        "Company Terminal",
        "Overview, funding, technology, competition, valuation history, notes, and reports."
    )'''

new = '''    section_title(
        "Company Intelligence Terminal",
        "Structured research, technology, funding, competition, valuation, notes, and report workspace."
    )'''

if old not in text:
    raise SystemExit("Could not find Company Terminal section title.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Company terminal section title polished.")
