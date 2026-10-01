from pathlib import Path
import re

path = Path("app.py")
text = path.read_text()

# Remove duplicate company_data import line.
text = text.replace(
    "from services.company_data import get_company_profiles, get_company_names\nfrom services.research_notes import",
    "from services.company_data import get_company_profiles, get_company_names\nfrom services.research_notes import",
    1,
)

# If duplicate still exists as standalone after research_notes import block, remove it.
lines = text.splitlines()
seen_company_import = False
cleaned = []
for line in lines:
    if line.strip() == "from services.company_data import get_company_profiles, get_company_names":
        if seen_company_import:
            continue
        seen_company_import = True
    cleaned.append(line)
text = "\n".join(cleaned) + "\n"

# Add company_name to valuation saves.
text = text.replace(
    '''save_valuation_supabase(
                valuation_type="standard_dcf",
            name=outputs["company_name"],
            payload={''',
    '''save_valuation_supabase(
                valuation_type="standard_dcf",
            name=outputs["company_name"],
            company_name=outputs["company_name"],
            payload={''',
    1,
)

text = text.replace(
    '''save_valuation_supabase(
                valuation_type="biotech_rnpv",
            name=outputs["asset_name"],
            payload={''',
    '''save_valuation_supabase(
                valuation_type="biotech_rnpv",
            name=outputs["asset_name"],
            company_name=outputs["asset_name"],
            payload={''',
    1,
)

# Add company_name to biotech uploads.
text = text.replace(
    '''                    file_bytes=rnpv_pdf,
                    mime_type="application/pdf",
                )''',
    '''                    file_bytes=rnpv_pdf,
                    mime_type="application/pdf",
                    company_name=asset_name,
                )''',
    1,
)

text = text.replace(
    '''                    file_bytes=biotech_excel,
                    mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )''',
    '''                    file_bytes=biotech_excel,
                    mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    company_name=asset_name,
                )''',
    1,
)

# Add company_name to standard DCF uploads.
text = text.replace(
    '''                    file_bytes=outputs["pdf"],
                    mime_type="application/pdf",
                )''',
    '''                    file_bytes=outputs["pdf"],
                    mime_type="application/pdf",
                    company_name=outputs["company_name"],
                )''',
    1,
)

text = text.replace(
    '''                    file_bytes=outputs["standard_excel"],
                    mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )''',
    '''                    file_bytes=outputs["standard_excel"],
                    mime_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    company_name=outputs["company_name"],
                )''',
    1,
)

path.write_text(text)
print("Patched app.py company_name call sites and cleaned duplicate import.")
