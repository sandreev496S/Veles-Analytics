from pathlib import Path

path = Path("components/dcf_steps/results_step.py")
text = path.read_text()

old_import = '''from components.ui.cards import kpi_card
from services.pdf_report import create_dcf_pdf'''

new_import = '''from components.ui.cards import kpi_card
from components.ui.panels import section_panel
from services.pdf_report import create_dcf_pdf'''

if old_import not in text:
    raise SystemExit("Could not find cards import.")

text = text.replace(old_import, new_import, 1)

replacements = {
'''        section_title(
            "Scenario Comparison",
            "Compare downside, base case, and upside valuation outcomes."
        )''':
'''        section_panel(
            "Scenario Comparison",
            "Compare downside, base case, and upside valuation outcomes."
        )''',

'''        section_title(
            "Base Case Forecast",
            "Revenue and free cash flow forecast for the base case."
        )''':
'''        section_panel(
            "Base Case Forecast",
            "Revenue and free cash flow forecast for the base case."
        )''',

'''        section_title(
            "Sensitivity Matrix",
            "Base case implied share price sensitivity."
        )''':
'''        section_panel(
            "Sensitivity Matrix",
            "Base case implied share price sensitivity."
        )''',

'''        section_title(
            "Reverse DCF — Implied Growth",
            "Revenue growth implied by the current market capitalization."
        )''':
'''        section_panel(
            "Reverse DCF — Implied Growth",
            "Revenue growth implied by the current market capitalization."
        )''',

'''        section_title(
            "Comparable Valuation",
            "Peer-derived valuation multiples and implied enterprise value outputs."
        )''':
'''        section_panel(
            "Comparable Valuation",
            "Peer-derived valuation multiples and implied enterprise value outputs."
        )''',

'''        section_title(
            "Charts",
            "Revenue, free cash flow, and enterprise value bridge."
        )''':
'''        section_panel(
            "Charts",
            "Revenue, free cash flow, and enterprise value bridge."
        )''',

'''    section_title(
        "Exports",
        "Download client-ready PDF and Excel valuation outputs."
    )''':
'''    section_panel(
        "Exports",
        "Download client-ready PDF and Excel valuation outputs."
    )''',
}

for old, new in replacements.items():
    if old in text:
        text = text.replace(old, new, 1)

path.write_text(text)

print("DCF Results page now uses reusable section panels.")
