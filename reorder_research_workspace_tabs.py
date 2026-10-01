from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    overview_tab, funding_tab, tech_tab, competition_tab, valuation_tab, notes_tab, reports_tab = st.tabs(
        [
            "Overview",
            "Technology",
            "Funding",
            "Competition",
            "Valuations",
            "Research Notes",
            "Reports",
        ]
    )'''

new = '''    overview_tab, tech_tab, funding_tab, competition_tab, valuation_tab, notes_tab, reports_tab = st.tabs(
        [
            "Overview",
            "Technology",
            "Funding",
            "Competition",
            "Valuations",
            "Research Notes",
            "Reports",
        ]
    )'''

if old not in text:
    raise SystemExit("Could not find research workspace tab assignment block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Research Workspace tab variables reordered to match labels.")
