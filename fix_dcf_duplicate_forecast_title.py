from pathlib import Path

path = Path("components/dcf_wizard.py")
text = path.read_text()

old = '''    if selected_step in ["2 · Forecast", "3 · Scenarios", "4 · Run Model", "5 · Results"]:
        section_title(
            "Step 2 — Forecast Assumptions",
            "Define downside, base, and upside case operating assumptions."
        )

'''

if old not in text:
    raise SystemExit("Duplicate forecast title block not found.")

text = text.replace(old, "", 1)
path.write_text(text)

print("Removed duplicate Step 2 forecast title block.")
