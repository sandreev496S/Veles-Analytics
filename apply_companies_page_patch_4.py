from pathlib import Path

path = Path("app.py")
text = path.read_text()

insert_after = '''                st.success(f"Added company: {new_name}")
                st.rerun()

'''

addition = '''    section_title(
        "Edit Company",
        "Update an existing company profile."
    )

    companies = list_companies()

    if companies:
        company_options = {
            company["name"]: company
            for company in companies
        }

        selected_edit_company = st.selectbox(
            "Select company to edit",
            list(company_options.keys()),
            key="edit_company_select",
        )

        selected_company_record = company_options[selected_edit_company]

        with st.form("edit_company_form"):
            col1, col2 = st.columns(2)

            with col1:
                edit_name = st.text_input("Company name", value=selected_company_record.get("name") or "")
                edit_sector = st.text_input("Sector", value=selected_company_record.get("sector") or "")
                edit_focus = st.text_input("Focus", value=selected_company_record.get("focus") or "")

            with col2:
                edit_modality = st.text_input("Modality", value=selected_company_record.get("modality") or "")
                edit_stage = st.text_input("Stage", value=selected_company_record.get("stage") or "")
                edit_funding = st.text_input("Funding", value=selected_company_record.get("funding") or "")
                edit_valuation = st.text_input("Valuation", value=selected_company_record.get("valuation") or "")
                edit_website = st.text_input("Website", value=selected_company_record.get("website") or "")

            edit_risk = st.text_area("Risk profile", value=selected_company_record.get("risk") or "")

            edit_submitted = st.form_submit_button("Update Company")

            if edit_submitted:
                update_company(
                    selected_company_record["id"],
                    name=edit_name,
                    sector=edit_sector,
                    focus=edit_focus,
                    modality=edit_modality,
                    stage=edit_stage,
                    funding=edit_funding,
                    valuation=edit_valuation,
                    risk=edit_risk,
                    website=edit_website,
                )
                st.success(f"Updated company: {edit_name}")
                st.rerun()
    else:
        activity_item(
            "No Companies Available",
            "Add a company before using the edit workflow.",
            "Company Database"
        )

'''

if insert_after not in text:
    raise SystemExit("Could not find Add Company success block.")

text = text.replace(insert_after, insert_after + addition, 1)
path.write_text(text)

print("Companies edit form added.")
