from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''            company_reports = [
                report for report in report_records
                if selected_company.lower() in str(report.get("file_name", "")).lower()
            ]'''

new = '''            company_reports = [
                report for report in report_records
                if (
                    str(report.get("company_name", "")).lower() == selected_company.lower()
                    or selected_company.lower() in str(report.get("file_name", "")).lower()
                )
            ]'''

if old not in text:
    raise SystemExit("Could not find filename-based reports filter.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Reports tab now filters by company_name with filename fallback.")
