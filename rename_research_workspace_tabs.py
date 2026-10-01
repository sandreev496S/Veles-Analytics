from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        [
            "Overview",
            "Funding",
            "Technology",
            "Competition",
            "Valuation History",
            "Notes",
            "Reports",
        ]'''

new = '''        [
            "Overview",
            "Technology",
            "Funding",
            "Competition",
            "Valuations",
            "Research Notes",
            "Reports",
        ]'''

if old not in text:
    raise SystemExit("Could not find research workspace tab labels.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Research Workspace tabs renamed.")
