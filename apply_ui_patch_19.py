from pathlib import Path

path = Path("app.py")
text = path.read_text()

replacements = [
    (
        'company_card("Neuralink", "Series D", "$6.1B valuation")',
        'company_card("Neuralink", "Series D", "$6.1B valuation", funding="$686M+")',
    ),
    (
        'company_card("Synchron", "Series C", "Private valuation")',
        'company_card("Synchron", "Series C", "Private valuation", funding="$145M+")',
    ),
    (
        'company_card("Paradromics", "Clinical-stage", "Private valuation")',
        'company_card("Paradromics", "Clinical-stage", "Private valuation", funding="$100M+")',
    ),
    (
        'company_card("Blackrock Neurotech", "Growth stage", "Private valuation")',
        'company_card("Blackrock Neurotech", "Growth stage", "Private valuation", funding="Private")',
    ),
    (
        'company_card("Precision Neuroscience", "Series B", "Private valuation")',
        'company_card("Precision Neuroscience", "Series B", "Private valuation", funding="$100M+")',
    ),
]

for old, new in replacements:
    if old not in text:
        print(f"Skipping missing block: {old}")
        continue
    text = text.replace(old, new)

path.write_text(text)
print("UI patch 19 applied: watchlist funding data added.")
