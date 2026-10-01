from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    watchlist_columns = st.columns(len(tracked_companies))

    for column, (company_name, company_data) in zip(watchlist_columns, tracked_companies.items()):
        with column:
            company_card(
                company_name,
                company_data["stage"],
                company_data["valuation"],
                funding=company_data["funding"],
            )'''

new = '''    if tracked_companies:
        watchlist_columns = st.columns(len(tracked_companies))

        for column, (company_name, company_data) in zip(watchlist_columns, tracked_companies.items()):
            with column:
                company_card(
                    company_name,
                    company_data["stage"],
                    company_data["valuation"],
                    funding=company_data["funding"],
                )
    else:
        activity_item(
            "No Companies Found",
            "Seed the companies table in Supabase to populate the Dashboard watchlist.",
            "Company Database"
        )'''

if old not in text:
    raise SystemExit("Could not find watchlist columns block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Dashboard now handles empty company database.")
