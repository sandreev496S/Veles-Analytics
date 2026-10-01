from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    tracked_companies = [
        "Neuralink",
        "Synchron",
        "Paradromics",
        "Blackrock Neurotech",
        "Precision Neuroscience",
    ]'''

new = '''    tracked_companies = {
        "Neuralink": {
            "stage": "Series D",
            "valuation": "$6.1B valuation",
            "funding": "$686M+",
        },
        "Synchron": {
            "stage": "Series C",
            "valuation": "Private valuation",
            "funding": "$145M+",
        },
        "Paradromics": {
            "stage": "Clinical-stage",
            "valuation": "Private valuation",
            "funding": "$100M+",
        },
        "Blackrock Neurotech": {
            "stage": "Growth stage",
            "valuation": "Private valuation",
            "funding": "Private",
        },
        "Precision Neuroscience": {
            "stage": "Series B",
            "valuation": "Private valuation",
            "funding": "$100M+",
        },
    }'''

if old not in text:
    raise SystemExit("Could not find tracked_companies list.")

text = text.replace(old, new, 1)

old2 = '''    with col3:
        metric_card("Coverage", len(tracked_companies), "Tracked Companies")'''

new2 = '''    with col3:
        metric_card("Coverage", len(tracked_companies.keys()), "Tracked Companies")'''

if old2 not in text:
    raise SystemExit("Could not find Coverage KPI len block.")

text = text.replace(old2, new2, 1)

watchlist_replacements = [
    (
        'company_card("Neuralink", "Series D", "$6.1B valuation", funding="$686M+")',
        'company_card("Neuralink", tracked_companies["Neuralink"]["stage"], tracked_companies["Neuralink"]["valuation"], funding=tracked_companies["Neuralink"]["funding"])',
    ),
    (
        'company_card("Synchron", "Series C", "Private valuation", funding="$145M+")',
        'company_card("Synchron", tracked_companies["Synchron"]["stage"], tracked_companies["Synchron"]["valuation"], funding=tracked_companies["Synchron"]["funding"])',
    ),
    (
        'company_card("Paradromics", "Clinical-stage", "Private valuation", funding="$100M+")',
        'company_card("Paradromics", tracked_companies["Paradromics"]["stage"], tracked_companies["Paradromics"]["valuation"], funding=tracked_companies["Paradromics"]["funding"])',
    ),
    (
        'company_card("Blackrock Neurotech", "Growth stage", "Private valuation", funding="Private")',
        'company_card("Blackrock Neurotech", tracked_companies["Blackrock Neurotech"]["stage"], tracked_companies["Blackrock Neurotech"]["valuation"], funding=tracked_companies["Blackrock Neurotech"]["funding"])',
    ),
    (
        'company_card("Precision Neuroscience", "Series B", "Private valuation", funding="$100M+")',
        'company_card("Precision Neuroscience", tracked_companies["Precision Neuroscience"]["stage"], tracked_companies["Precision Neuroscience"]["valuation"], funding=tracked_companies["Precision Neuroscience"]["funding"])',
    ),
]

for old_call, new_call in watchlist_replacements:
    if old_call not in text:
        print(f"Skipping missing call: {old_call}")
        continue
    text = text.replace(old_call, new_call, 1)

path.write_text(text)
print("UI patch 37 applied: dashboard watchlist uses centralized company data.")
