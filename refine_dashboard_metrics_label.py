from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title(
        "Platform Overview",
        "Operational metrics across valuation, reports, coverage, and system readiness."
    )'''

new = '''    section_title(
        "Operating Metrics",
        "Current platform coverage, saved models, report output, and system readiness."
    )'''

if old not in text:
    raise SystemExit("Could not find Platform Overview section title.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Dashboard metrics section label refined.")
