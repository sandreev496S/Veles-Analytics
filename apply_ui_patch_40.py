from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    k1, k2, k3, k4 = st.columns(4)

    with k1:
        metric_card("Company", selected_company, "Selected")

    with k2:
        metric_card("Modality", selected_profile["modality"], "Technology")

    with k3:
        metric_card("Stage", selected_profile["stage"], "Tracked")

    with k4:
        metric_card("Funding", selected_profile["funding"], "Known Capital")'''

new = '''    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        metric_card("Company", selected_company, "Selected")

    with k2:
        metric_card("Modality", selected_profile["modality"], "Technology")

    with k3:
        metric_card("Stage", selected_profile["stage"], "Tracked")

    with k4:
        metric_card("Funding", selected_profile["funding"], "Known Capital")

    with k5:
        metric_card("Valuation", selected_profile["valuation"], "Latest Known")'''

if old not in text:
    raise SystemExit("Could not find Research Workspace KPI row.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 40 applied: valuation KPI added to Research Workspace.")
