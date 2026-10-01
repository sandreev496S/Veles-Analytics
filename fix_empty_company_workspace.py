from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    selected_company = st.selectbox(
        "Select company",
        list(company_profiles.keys()),
    )

    selected_profile = company_profiles[selected_company]'''

new = '''    if not company_profiles:
        activity_item(
            "No Companies Found",
            "Seed the companies table in Supabase before using the Research Workspace.",
            "Company Database"
        )
        st.stop()

    selected_company = st.selectbox(
        "Select company",
        list(company_profiles.keys()),
    )

    if not selected_company:
        activity_item(
            "No Company Selected",
            "Select a company to open its research workspace.",
            "Company Database"
        )
        st.stop()

    selected_profile = company_profiles[selected_company]'''

if old not in text:
    raise SystemExit("Could not find Research Workspace company selector block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Research Workspace now handles empty company database.")
