from pathlib import Path

path = Path("components/dcf_wizard.py")
text = path.read_text()

old_import = '''from components.ui.workflow import render_workflow_progress, render_workflow_cards'''

new_import = '''from components.ui.workflow import render_workflow_progress, render_workflow_cards
from components.ui.cards import glass_card'''

if old_import not in text:
    raise SystemExit("Could not find workflow import.")

text = text.replace(old_import, new_import, 1)

old = '''    if selected_step == "4 · Run Model":
        section_title(
            "Step 4 — Run Model",
            "Generate scenario outputs, sensitivity analysis, comparables, charts, and exports."
        )'''

new = '''    if selected_step == "4 · Run Model":
        section_title(
            "Step 4 — Run Model",
            "Generate scenario outputs, sensitivity analysis, comparables, charts, and exports."
        )

        glass_card(
            title="Ready to Generate Institutional Valuation",
            eyebrow="Run Model",
            body="Veles will validate company inputs, merge forecast and valuation assumptions, run downside/base/upside DCF cases, build sensitivity analysis, calculate reverse DCF implied growth, generate comparable valuation outputs, and prepare exports."
        )'''

if old not in text:
    raise SystemExit("Could not find Step 4 section block.")

text = text.replace(old, new, 1)

path.write_text(text)

print("Added institutional run model card to DCF wizard.")
