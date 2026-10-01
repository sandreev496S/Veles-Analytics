from pathlib import Path

path = Path("app.py")
text = path.read_text()

# Insert default action after companies are loaded.
text = text.replace(
'''    companies = list_companies()

    st.markdown(''',
'''    companies = list_companies()
    st.session_state.setdefault("companies_action", "add")

    st.markdown(''',
1
)

# Replace Open Company Workspace block position with action launcher first.
old = '''    section_title(
        "Open Company Workspace",
        "Use the Research Workspace page to open a full company terminal."
    )'''

new = '''    section_title(
        "Company Actions",
        "Choose an action to manage the company intelligence database."
    )

    action_col1, action_col2, action_col3 = st.columns(3)

    with action_col1:
        if st.button("＋ Add Company", key="companies_action_add", use_container_width=True):
            st.session_state["companies_action"] = "add"
            st.rerun()

    with action_col2:
        if st.button("✎ Edit Company", key="companies_action_edit", use_container_width=True):
            st.session_state["companies_action"] = "edit"
            st.rerun()

    with action_col3:
        if st.button("⌫ Delete Company", key="companies_action_delete", use_container_width=True):
            st.session_state["companies_action"] = "delete"
            st.rerun()

    section_title(
        "Workspace Launcher",
        "Open a company in the Research Workspace."
    )'''

if old not in text:
    raise SystemExit("Could not find Open Company Workspace section title.")

text = text.replace(old, new, 1)

# Wrap Add Company section.
text = text.replace(
'''    section_title(
        "Add Company",
        "Create a new company profile for the research workspace."
    )

    with st.form("add_company_form"):''',
'''    if st.session_state.get("companies_action") == "add":
        section_title(
            "Add Company",
            "Create a new company profile for the research workspace."
        )

        with st.form("add_company_form"):''',
1
)

# Indent Add form block until Edit Company title.
start = text.index('''        with st.form("add_company_form"):''')
end = text.index('''    section_title(
        "Edit Company",''', start)
block = text[start:end]
text = text[:start] + "\n".join(("    " + line if line.strip() else line) for line in block.splitlines()) + text[end:]

# Wrap Edit Company section.
text = text.replace(
'''    section_title(
        "Edit Company",
        "Update an existing company profile."
    )''',
'''    if st.session_state.get("companies_action") == "edit":
        section_title(
            "Edit Company",
            "Update an existing company profile."
        )''',
1
)

start = text.index('''        section_title(
            "Edit Company",''')
end = text.index('''    section_title(
        "Delete Company",''', start)
block = text[start:end]
text = text[:start] + "\n".join(("    " + line if line.strip() else line) for line in block.splitlines()) + text[end:]

# Wrap Delete Company section.
text = text.replace(
'''    section_title(
        "Delete Company",
        "Remove a company from the intelligence database."
    )''',
'''    if st.session_state.get("companies_action") == "delete":
        section_title(
            "Delete Company",
            "Remove a company from the intelligence database."
        )''',
1
)

start = text.index('''        section_title(
            "Delete Company",''')
end = text.index('''elif page == "Research Workspace":''', start)
block = text[start:end]
text = text[:start] + "\n".join(("    " + line if line.strip() else line) for line in block.splitlines()) + "\n\n" + text[end:]

path.write_text(text)
print("Companies page now uses action launcher workflow.")
