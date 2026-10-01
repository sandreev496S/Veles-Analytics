from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    selected_company = st.selectbox(
        "Select company",
        [
            "Neuralink",
            "Synchron",
            "Paradromics",
            "Blackrock Neurotech",
            "Precision Neuroscience",
        ],
    )'''

new = '''    company_profiles = {
        "Neuralink": {
            "stage": "Series D",
            "focus": "Implantable BCI",
            "risk": "Regulatory and surgical adoption risk",
        },
        "Synchron": {
            "stage": "Clinical-stage",
            "focus": "Endovascular BCI",
            "risk": "Clinical validation and commercialization risk",
        },
        "Paradromics": {
            "stage": "Clinical-stage",
            "focus": "High-bandwidth implantable BCI",
            "risk": "Technical execution and trial progression risk",
        },
        "Blackrock Neurotech": {
            "stage": "Growth stage",
            "focus": "Neural interfaces and research systems",
            "risk": "Competitive positioning and scaling risk",
        },
        "Precision Neuroscience": {
            "stage": "Series B",
            "focus": "Minimally invasive BCI",
            "risk": "Regulatory pathway and market adoption risk",
        },
    }

    selected_company = st.selectbox(
        "Select company",
        list(company_profiles.keys()),
    )

    selected_profile = company_profiles[selected_company]'''

if old not in text:
    raise SystemExit("Could not find selected company block.")

text = text.replace(old, new, 1)

text = text.replace(
    'metric_card("Stage", "Private", "Tracked")',
    'metric_card("Stage", selected_profile["stage"], "Tracked")',
    1,
)

text = text.replace(
    '''            f"{selected_company} is tracked inside the Veles neurotechnology research universe. This workspace will consolidate company profile data, funding history, technology notes, valuation outputs, and generated reports."''',
    '''            f"{selected_company} is tracked inside the Veles neurotechnology research universe. Focus area: {selected_profile['focus']}. This workspace consolidates company profile data, funding history, technology notes, valuation outputs, and generated reports."''',
    1,
)

text = text.replace(
    '''            "Regulatory, clinical, technical, and commercialization risks will be summarized here.",''',
    '''            selected_profile["risk"],''',
    1,
)

path.write_text(text)

print("UI patch 25 applied: Research Workspace company data is now dynamic.")
