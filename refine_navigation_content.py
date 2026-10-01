from pathlib import Path

path = Path("components/ui/navigation.py")
text = path.read_text()

old = '''NAV_SECTIONS = [
    {
        "label": "Workspace",
        "items": [
            ("Dashboard", "⌂"),
        ],
    },
    {
        "label": "Research",
        "items": [
            ("Companies", "◈"),
            ("Research Workspace", "◉"),
        ],
    },
    {
        "label": "Valuation",
        "items": [
            ("Standard DCF", "◌"),
            ("Biotech rNPV", "◍"),
        ],
    },
    {
        "label": "Reports",
        "items": [
            ("Saved Models", "◫"),
            ("Saved Reports", "◫"),
        ],
    },
    {
        "label": "Platform",
        "items": [
            ("Settings", "⚙"),
            ("Methodology", "ⓘ"),
        ],
    },
]'''

new = '''NAV_SECTIONS = [
    {
        "label": "Command",
        "items": [
            ("Dashboard", "⌂"),
        ],
    },
    {
        "label": "Research",
        "items": [
            ("Companies", "◈"),
            ("Research Workspace", "◉"),
        ],
    },
    {
        "label": "Valuation",
        "items": [
            ("Standard DCF", "◌"),
            ("Biotech rNPV", "◍"),
        ],
    },
    {
        "label": "Library",
        "items": [
            ("Saved Models", "◫"),
            ("Saved Reports", "▤"),
        ],
    },
    {
        "label": "Platform",
        "items": [
            ("Settings", "⚙"),
            ("Methodology", "ⓘ"),
        ],
    },
]'''

if old not in text:
    raise SystemExit("Could not find the existing NAV_SECTIONS block. Paste navigation.py if this fails.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Navigation content refined.")
