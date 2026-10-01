from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    profile_col, risk_col, action_col = st.columns([2, 1, 1])'''

new = '''    section_title(
        "Company Snapshot",
        "High-level institutional profile for the selected company."
    )

    profile_col, risk_col, action_col = st.columns([2, 1, 1])'''

if old not in text:
    raise SystemExit("Could not find Research Workspace profile column block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 24 applied: Company Snapshot section added.")
