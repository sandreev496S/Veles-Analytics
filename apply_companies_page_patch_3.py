from pathlib import Path

path = Path("app.py")
text = path.read_text()

marker = '''elif page == "Research Workspace":'''

companies_page = '''elif page == "Companies":

    page_header(
        "Companies",
        "Manage the company intelligence database used across Veles."
    )

    section_title(
        "Company Database",
        "Add, review, and manage tracked neurotechnology and biotech companies."
    )

    companies = list_companies()

    if companies:
        companies_df = pd.DataFrame(companies)
        st.dataframe(companies_df, use_container_width=True)
    else:
        activity_item(
            "No Companies Found",
            "Add your first company below to populate the research workspace.",
            "Company Database"
        )

    section_title(
        "Add Company",
        "Create a new company profile for the research workspace."
    )

    with st.form("add_company_form"):
        col1, col2 = st.columns(2)

        with col1:
            new_name = st.text_input("Company name")
            new_sector = st.text_input("Sector", value="Neurotechnology")
            new_focus = st.text_input("Focus")

        with col2:
            new_modality = st.text_input("Modality")
            new_stage = st.text_input("Stage")
            new_funding = st.text_input("Funding")
            new_valuation = st.text_input("Valuation")
            new_website = st.text_input("Website")

        new_risk = st.text_area("Risk profile")

        submitted = st.form_submit_button("Add Company")

        if submitted:
            if not new_name:
                st.error("Company name is required.")
            else:
                create_company(
                    name=new_name,
                    sector=new_sector,
                    focus=new_focus,
                    modality=new_modality,
                    stage=new_stage,
                    funding=new_funding,
                    valuation=new_valuation,
                    risk=new_risk,
                    website=new_website,
                )
                st.success(f"Added company: {new_name}")
                st.rerun()

'''

if marker not in text:
    raise SystemExit("Could not find Research Workspace marker.")

text = text.replace(marker, companies_page + marker, 1)
path.write_text(text)

print("Companies page body added.")
