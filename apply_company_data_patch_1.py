from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''from services.biotech_rnpv import run_biotech_rnpv, rnpv_sensitivity_matrix, run_monte_carlo_rnpv, biotech_tornado_analysis'''

new = '''from services.biotech_rnpv import run_biotech_rnpv, rnpv_sensitivity_matrix, run_monte_carlo_rnpv, biotech_tornado_analysis
from services.company_data import get_company_profiles, get_company_names'''

if old not in text:
    raise SystemExit("Could not find biotech_rnpv import line.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Company data imports added.")
