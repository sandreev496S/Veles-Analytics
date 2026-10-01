from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''from services.company_data import get_company_profiles, get_company_names'''

new = '''from services.company_data import get_company_profiles, get_company_names
from services.research_notes import (
    load_research_note,
    save_research_note,
    list_research_notes,
    delete_research_note,
)'''

if old not in text:
    raise SystemExit("Could not find company_data import line.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Research notes service imported.")
