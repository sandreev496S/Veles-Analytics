from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with tech_tab:
        metric_card("Modality", selected_profile["modality"], selected_profile["focus"])

        activity_item(
            "Technology Profile",
            "Device type, invasiveness, patents, technical differentiation, and relevant research papers will be organized here.",
            "Technical"
        )'''

new = '''    with tech_tab:
        metric_card("Modality", selected_profile["modality"], selected_profile["focus"])

        technology_profile = pd.DataFrame([
            {
                "Company": selected_company,
                "Focus": selected_profile["focus"],
                "Modality": selected_profile["modality"],
                "Invasiveness": selected_profile["modality"],
                "Technical Status": "Tracked",
            }
        ])

        st.dataframe(technology_profile, use_container_width=True)

        activity_item(
            "Technology Profile",
            "This table is currently seeded from the company profile map. Next step: connect patents, papers, device specs, and clinical data.",
            "Technical"
        )'''

if old not in text:
    raise SystemExit("Could not find Technology tab block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 42 applied: Technology tab now includes a structured profile table.")
