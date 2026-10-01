from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        ai_workflow_card(
            "AI Analyst Workflow",
            [
                "Monitoring neurotechnology company coverage",
                "Reviewing valuation model activity",
                "Tracking generated reports and exports",
                "Preparing research workspace updates",
            ],
        )

'''

if old not in text:
    raise SystemExit("Could not find AI workflow block.")

text = text.replace(old, "", 1)
path.write_text(text)

print("UI patch 16 applied: removed AI workflow block from Dashboard.")
