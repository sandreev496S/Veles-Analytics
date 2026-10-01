from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with activity_col:
        activity_item(
            "Generated Research Report",
            "A new AI-assisted company research report was created and prepared for export.",
            "Reports"
        )

        activity_item(
            "Updated Company Coverage",
            "Neurotechnology company watchlist refreshed with core BCI competitors.",
            "Workspace"
        )

    with model_col:
        activity_item(
            "Saved Valuation Model",
            "Latest DCF and rNPV models will appear here after being saved.",
            "Saved Models"
        )

        activity_item(
            "Monte Carlo Simulation",
            "Simulation outputs and probability distributions will be surfaced here.",
            "Analysis"
        )'''

new = '''    with activity_col:
        activity_item(
            "Generated Neuralink DCF",
            "Base case intrinsic valuation model created with scenario comparison and sensitivity matrix.",
            "Valuation"
        )

        activity_item(
            "Updated Neurotech Watchlist",
            "Core BCI competitor universe refreshed for company research tracking.",
            "Workspace"
        )

    with model_col:
        activity_item(
            "Saved Biotech rNPV Model",
            "Risk-adjusted valuation model saved for future analysis and report generation.",
            "Saved Models"
        )

        activity_item(
            "Prepared Monte Carlo Output",
            "Simulation distribution and percentile table ready for analyst review.",
            "Analysis"
        )'''

if old not in text:
    raise SystemExit("Could not find Recent Activity placeholder block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 20 applied: recent activity upgraded.")
