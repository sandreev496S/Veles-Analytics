from pathlib import Path

path = Path("components/dcf_steps/results_step.py")
text = path.read_text()

text = text.replace(
'''    section_title(
        "Step 5 — Results",
        "Review valuation outputs, sensitivity analysis, comparables, exports, and saved model data."
    )''',
'''    section_title(
        "Step 5 — Valuation Results",
        "Review intrinsic value, scenario outputs, sensitivity analysis, comparables, charts, and exports."
    )''',
1
)

text = text.replace(
'''        section_panel(
            "Scenario Comparison",
            "Compare downside, base case, and upside valuation outcomes."
        )''',
'''        section_panel(
            "Scenario Output",
            "Compare downside, base case, and upside valuation outcomes."
        )''',
1
)

text = text.replace(
'''        section_panel(
            "Base Case Forecast",
            "Revenue and free cash flow forecast for the base case."
        )''',
'''        section_panel(
            "Base Case Operating Forecast",
            "Revenue and free cash flow forecast for the base case."
        )''',
1
)

text = text.replace(
'''        section_panel(
            "Comparable Valuation",
            "Peer-derived valuation multiples and implied enterprise value outputs."
        )''',
'''        section_panel(
            "Comparable Company Valuation",
            "Peer-derived valuation multiples and implied enterprise value outputs."
        )''',
1
)

text = text.replace(
'''    section_panel(
        "Exports",
        "Download client-ready PDF and Excel valuation outputs."
    )''',
'''    section_panel(
        "Export Center",
        "Download client-ready PDF and Excel valuation outputs."
    )''',
1
)

path.write_text(text)
print("DCF results step polished.")
