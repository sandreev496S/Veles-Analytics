COMPANY_PROFILES = {
    "Neuralink": {
        "stage": "Series D",
        "focus": "Implantable BCI",
        "modality": "Invasive",
        "funding": "$686M+",
        "valuation": "$6.1B valuation",
        "risk": "Regulatory and surgical adoption risk",
    },
    "Synchron": {
        "stage": "Clinical-stage",
        "focus": "Endovascular BCI",
        "modality": "Minimally invasive",
        "funding": "$145M+",
        "valuation": "Private valuation",
        "risk": "Clinical validation and commercialization risk",
    },
    "Paradromics": {
        "stage": "Clinical-stage",
        "focus": "High-bandwidth implantable BCI",
        "modality": "Invasive",
        "funding": "$100M+",
        "valuation": "Private valuation",
        "risk": "Technical execution and trial progression risk",
    },
    "Blackrock Neurotech": {
        "stage": "Growth stage",
        "focus": "Neural interfaces and research systems",
        "modality": "Invasive",
        "funding": "Private",
        "valuation": "Private valuation",
        "risk": "Competitive positioning and scaling risk",
    },
    "Precision Neuroscience": {
        "stage": "Series B",
        "focus": "Minimally invasive BCI",
        "modality": "Minimally invasive",
        "funding": "$100M+",
        "valuation": "Private valuation",
        "risk": "Regulatory pathway and market adoption risk",
    },
}


def get_company_profiles():
    return COMPANY_PROFILES


def get_company_names():
    return list(COMPANY_PROFILES.keys())


def get_company_profile(company_name):
    return COMPANY_PROFILES.get(company_name)
