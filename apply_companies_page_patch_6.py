from pathlib import Path

path = Path("app.py")
text = path.read_text()

insert_after = '''    if companies:
        companies_df = pd.DataFrame(companies)
        st.dataframe(companies_df, use_container_width=True)
    else:
        activity_item(
            "No Companies Found",
            "Add your first company below to populate the research workspace.",
            "Company Database"
        )

'''

addition = '''    section_title(
        "Open Company Workspace",
        "Use the Research Workspace page to open a full company terminal."
    )

    if companies:
        workspace_company = st.selectbox(
            "Choose company to research",
            [company["name"] for company in companies],
            key="companies_workspace_select",
        )

        activity_item(
            f"Open {workspace_company}",
            "Go to Research Workspace from the sidebar and select this company to view reports, models, notes, funding, technology, and competition.",
            "Research Workspace"
        )
    else:
        activity_item(
            "No Workspace Available",
            "Add a company first to enable research workspace navigation.",
            "Research Workspace"
        )

'''

if insert_after not in text:
    raise SystemExit("Could not find Companies table block.")

text = text.replace(insert_after, insert_after + addition, 1)
path.write_text(text)

print("Companies workspace shortcut section added.")
