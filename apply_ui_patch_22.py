from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title(
        selected_company,
        "Unified research profile"
    )

    profile_col, risk_col, action_col = st.columns([2, 1, 1])'''

new = '''    section_title(
        selected_company,
        "Unified research profile"
    )

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        metric_card("Company", selected_company, "Selected")

    with k2:
        metric_card("Sector", "BCI", "Neurotech")

    with k3:
        metric_card("Stage", "Private", "Tracked")

    with k4:
        metric_card("Coverage", "Active", "Workspace")

    profile_col, risk_col, action_col = st.columns([2, 1, 1])'''

if old not in text:
    raise SystemExit("Could not find Research Workspace header block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 22 applied: Research Workspace KPI header added.")
