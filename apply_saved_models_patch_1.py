from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''            company_records = [
                record for record in valuation_records
                if selected_company.lower() in str(record.get("name", "")).lower()
            ]'''

new = '''            company_records = [
                record for record in valuation_records
                if (
                    str(record.get("company_name", "")).lower() == selected_company.lower()
                    or selected_company.lower() in str(record.get("name", "")).lower()
                )
            ]'''

if old not in text:
    raise SystemExit("Could not find filename/name-based valuation filter block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Valuation History tab now filters by company_name with name fallback.")
