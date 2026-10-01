from pathlib import Path

path = Path("app.py")
text = path.read_text()

start_marker = '''    tracked_companies = {
        "Neuralink": {
            "stage": "Series D",
            "valuation": "$6.1B valuation",
            "funding": "$686M+",
        },'''

end_marker = '''        },
    }'''

if start_marker not in text:
    raise SystemExit("Could not find tracked_companies dictionary start.")

start = text.index(start_marker)
end = text.index(end_marker, start) + len(end_marker)

new_block = '''    tracked_companies = get_company_profiles()'''

text = text[:start] + new_block + text[end:]

path.write_text(text)

print("Dashboard tracked_companies now uses get_company_profiles().")
