from pathlib import Path

path = Path("app.py")
text = path.read_text()

# Remove Companies KPI strip.
old_metrics = '''    stages = len(set([company.get("stage") for company in companies if company.get("stage")])) if companies else 0
    modalities = len(set([company.get("modality") for company in companies if company.get("modality")])) if companies else 0

    cov1, cov2, cov3, cov4 = st.columns(4)

    with cov1:
        metric_card("Tracked Companies", len(companies), "Coverage Universe")

    with cov2:
        metric_card("Stages", stages, "Company Maturity")

    with cov3:
        metric_card("Modalities", modalities, "Technology Types")

    with cov4:
        metric_card("Database", "Online", "Supabase")

'''

if old_metrics in text:
    text = text.replace(old_metrics, "", 1)
else:
    print("Companies KPI strip block not found; skipping.")

# Remove raw SQL-looking company dataframe block.
old_table = '''    section_title(
        "Company Universe",
        "Review and manage tracked neurotechnology and biotech companies."
    )

    if companies:
        companies_df = pd.DataFrame(companies)
        st.dataframe(companies_df, use_container_width=True)
    else:
        activity_item(
            "No Companies Found",
            "Add your first company below to populate the research workspace.",
            "Company Database"
        )

'''

new_table = '''    if not companies:
        activity_item(
            "No Companies Found",
            "Add your first company below to populate the research workspace.",
            "Company Database"
        )

'''

if old_table not in text:
    raise SystemExit("Could not find Company Universe dataframe block.")

text = text.replace(old_table, new_table, 1)

path.write_text(text)
print("Companies page simplified: removed KPI strip and raw dataframe block.")
