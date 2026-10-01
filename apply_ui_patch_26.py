from pathlib import Path

path = Path("app.py")
text = path.read_text()

replacements = [
    (
        '''"Neuralink": {
            "stage": "Series D",
            "focus": "Implantable BCI",
            "risk": "Regulatory and surgical adoption risk",
        },''',
        '''"Neuralink": {
            "stage": "Series D",
            "focus": "Implantable BCI",
            "modality": "Invasive",
            "funding": "$686M+",
            "risk": "Regulatory and surgical adoption risk",
        },''',
    ),
    (
        '''"Synchron": {
            "stage": "Clinical-stage",
            "focus": "Endovascular BCI",
            "risk": "Clinical validation and commercialization risk",
        },''',
        '''"Synchron": {
            "stage": "Clinical-stage",
            "focus": "Endovascular BCI",
            "modality": "Minimally invasive",
            "funding": "$145M+",
            "risk": "Clinical validation and commercialization risk",
        },''',
    ),
    (
        '''"Paradromics": {
            "stage": "Clinical-stage",
            "focus": "High-bandwidth implantable BCI",
            "risk": "Technical execution and trial progression risk",
        },''',
        '''"Paradromics": {
            "stage": "Clinical-stage",
            "focus": "High-bandwidth implantable BCI",
            "modality": "Invasive",
            "funding": "$100M+",
            "risk": "Technical execution and trial progression risk",
        },''',
    ),
    (
        '''"Blackrock Neurotech": {
            "stage": "Growth stage",
            "focus": "Neural interfaces and research systems",
            "risk": "Competitive positioning and scaling risk",
        },''',
        '''"Blackrock Neurotech": {
            "stage": "Growth stage",
            "focus": "Neural interfaces and research systems",
            "modality": "Invasive",
            "funding": "Private",
            "risk": "Competitive positioning and scaling risk",
        },''',
    ),
    (
        '''"Precision Neuroscience": {
            "stage": "Series B",
            "focus": "Minimally invasive BCI",
            "risk": "Regulatory pathway and market adoption risk",
        },''',
        '''"Precision Neuroscience": {
            "stage": "Series B",
            "focus": "Minimally invasive BCI",
            "modality": "Minimally invasive",
            "funding": "$100M+",
            "risk": "Regulatory pathway and market adoption risk",
        },''',
    ),
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f"Could not find profile block:\n{old}")
    text = text.replace(old, new, 1)

old_kpis = '''    with k2:
        metric_card("Sector", "BCI", "Neurotech")

    with k3:
        metric_card("Stage", selected_profile["stage"], "Tracked")

    with k4:
        metric_card("Coverage", "Active", "Workspace")'''

new_kpis = '''    with k2:
        metric_card("Modality", selected_profile["modality"], "Technology")

    with k3:
        metric_card("Stage", selected_profile["stage"], "Tracked")

    with k4:
        metric_card("Funding", selected_profile["funding"], "Known Capital")'''

if old_kpis not in text:
    raise SystemExit("Could not find Research Workspace KPI block.")

text = text.replace(old_kpis, new_kpis, 1)

path.write_text(text)
print("UI patch 26 applied: company funding and modality added.")
