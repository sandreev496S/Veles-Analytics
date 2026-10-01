from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        metric_card("Company", selected_company, "Selected")

    with k2:
        metric_card("Modality", selected_profile["modality"], "Technology")

    with k3:
        metric_card("Stage", selected_profile["stage"], "Tracked")

    with k4:
        metric_card("Funding", selected_profile["funding"], "Known Capital")

    with k5:
        metric_card("Valuation", selected_profile["valuation"], "Latest Known")
'''

new = '''    k1, k2, k3, k4, k5 = st.columns(5)

    with k1:
        metric_card("Technology", selected_profile["modality"], "Modality")

    with k2:
        metric_card("Stage", selected_profile["stage"], "Company Status")

    with k3:
        metric_card("Funding", selected_profile["funding"], "Known Capital")

    with k4:
        metric_card("Valuation", selected_profile["valuation"], "Latest Known")

    with k5:
        metric_card("Risk", selected_profile["risk"], "Research Flag")
'''

if old not in text:
    raise SystemExit("Could not find current company KPI strip.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Company terminal KPI strip refined.")
