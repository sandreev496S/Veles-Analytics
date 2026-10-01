from pathlib import Path

path = Path("app.py")
text = path.read_text()

insert_after = '''    else:
        activity_item(
            "No Companies Available",
            "Add a company before using the edit workflow.",
            "Company Database"
        )

'''

addition = '''    section_title(
        "Delete Company",
        "Remove a company from the intelligence database."
    )

    companies = list_companies()

    if companies:
        delete_options = {
            company["name"]: company
            for company in companies
        }

        selected_delete_company = st.selectbox(
            "Select company to delete",
            list(delete_options.keys()),
            key="delete_company_select",
        )

        selected_delete_record = delete_options[selected_delete_company]

        st.warning(
            "Deleting a company removes it from the company database. Existing reports, notes, and valuations may still remain separately stored."
        )

        confirm_delete = st.checkbox(
            f"I understand and want to delete {selected_delete_company}",
            key="confirm_delete_company",
        )

        if st.button("Delete Company", key="delete_company_button"):
            if not confirm_delete:
                st.error("Confirm deletion before continuing.")
            else:
                delete_company(selected_delete_record["id"])
                st.success(f"Deleted company: {selected_delete_company}")
                st.rerun()
    else:
        activity_item(
            "No Companies Available",
            "There are no companies available to delete.",
            "Company Database"
        )

'''

if insert_after not in text:
    raise SystemExit("Could not find edit workflow ending block.")

text = text.replace(insert_after, insert_after + addition, 1)
path.write_text(text)

print("Companies delete workflow added.")
