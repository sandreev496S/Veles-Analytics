from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''        "Neuralink": {
            "stage": "Series D",
            "focus": "Implantable BCI",
            "modality": "Invasive",
            "funding": "$686M+",
            "risk": "Regulatory and surgical adoption risk",
        },'''

new = '''        "Neuralink": {
            "stage": "Series D",
            "focus": "Implantable BCI",
            "modality": "Invasive",
            "funding": "$686M+",
            "valuation": "$6.1B valuation",
            "risk": "Regulatory and surgical adoption risk",
        },'''

if old not in text:
    raise SystemExit("Could not find Neuralink profile block.")

text = text.replace(old, new, 1)

old2 = '''        "Synchron": {
            "stage": "Clinical-stage",
            "focus": "Endovascular BCI",
            "modality": "Minimally invasive",
            "funding": "$145M+",
            "risk": "Clinical validation and commercialization risk",
        },'''

new2 = '''        "Synchron": {
            "stage": "Clinical-stage",
            "focus": "Endovascular BCI",
            "modality": "Minimally invasive",
            "funding": "$145M+",
            "valuation": "Private valuation",
            "risk": "Clinical validation and commercialization risk",
        },'''

text = text.replace(old2, new2, 1)

old3 = '''        "Paradromics": {
            "stage": "Clinical-stage",
            "focus": "High-bandwidth implantable BCI",
            "modality": "Invasive",
            "funding": "$100M+",
            "risk": "Technical execution and trial progression risk",
        },'''

new3 = '''        "Paradromics": {
            "stage": "Clinical-stage",
            "focus": "High-bandwidth implantable BCI",
            "modality": "Invasive",
            "funding": "$100M+",
            "valuation": "Private valuation",
            "risk": "Technical execution and trial progression risk",
        },'''

text = text.replace(old3, new3, 1)

old4 = '''        "Blackrock Neurotech": {
            "stage": "Growth stage",
            "focus": "Neural interfaces and research systems",
            "modality": "Invasive",
            "funding": "Private",
            "risk": "Competitive positioning and scaling risk",
        },'''

new4 = '''        "Blackrock Neurotech": {
            "stage": "Growth stage",
            "focus": "Neural interfaces and research systems",
            "modality": "Invasive",
            "funding": "Private",
            "valuation": "Private valuation",
            "risk": "Competitive positioning and scaling risk",
        },'''

text = text.replace(old4, new4, 1)

old5 = '''        "Precision Neuroscience": {
            "stage": "Series B",
            "focus": "Minimally invasive BCI",
            "modality": "Minimally invasive",
            "funding": "$100M+",
            "risk": "Regulatory pathway and market adoption risk",
        },'''

new5 = '''        "Precision Neuroscience": {
            "stage": "Series B",
            "focus": "Minimally invasive BCI",
            "modality": "Minimally invasive",
            "funding": "$100M+",
            "valuation": "Private valuation",
            "risk": "Regulatory pathway and market adoption risk",
        },'''

text = text.replace(old5, new5, 1)

path.write_text(text)
print("UI patch 39 applied: Research Workspace profiles now include valuation field.")
