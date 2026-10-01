from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with tech_tab:
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
        )
'''

new = '''    with tech_tab:
        section_title(
            "Technology Profile",
            "Modality, focus area, technical positioning, advantages, and research risks."
        )

        tech_k1, tech_k2, tech_k3 = st.columns(3)

        with tech_k1:
            metric_card("Modality", selected_profile["modality"], "Technology Type")

        with tech_k2:
            metric_card("Focus", selected_profile["focus"], "Use Case")

        with tech_k3:
            metric_card("Status", selected_profile["stage"], "Clinical / Company Stage")

        tech_left, tech_right = st.columns([1.35, 1])

        with tech_left:
            insight_card(
                "Technology Intelligence",
                f"{selected_company}'s technical diligence should focus on modality, invasiveness, signal quality, surgical burden, device durability, software stack, neural data infrastructure, and scalability of deployment."
            )

            technology_profile = pd.DataFrame([
                {
                    "Company": selected_company,
                    "Focus": selected_profile["focus"],
                    "Modality": selected_profile["modality"],
                    "Technical Status": "Tracked",
                    "Clinical / Company Stage": selected_profile["stage"],
                    "Primary Risk": selected_profile["risk"],
                }
            ])

            st.dataframe(technology_profile, use_container_width=True)

        with tech_right:
            activity_item(
                "Potential Advantages",
                "Assess differentiation in signal acquisition, hardware design, implantation burden, usability, software integration, and defensibility of neural datasets.",
                "Advantage"
            )

            activity_item(
                "Technical Risks",
                selected_profile["risk"],
                "Risk"
            )

            activity_item(
                "Next Data Sources",
                "Connect patents, papers, device specifications, clinical trial updates, FDA filings, and technical publications.",
                "Data Pipeline"
            )
'''

if old not in text:
    raise SystemExit("Could not find current technology tab block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Research Workspace technology tab redesigned.")
