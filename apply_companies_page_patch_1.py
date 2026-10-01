from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''from services.company_repository import get_company_profiles, get_company_names'''

new = '''from services.company_repository import (
    get_company_profiles,
    get_company_names,
    list_companies,
    create_company,
    update_company,
    delete_company,
)'''

if old not in text:
    raise SystemExit("Could not find company_repository import line.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Company CRUD imports added.")
