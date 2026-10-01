from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    w1, w2, w3, w4, w5 = st.columns(5)

    with w1:
        company_card("Neuralink", tracked_companies["Neuralink"]["stage"], tracked_companies["Neuralink"]["valuation"], funding=tracked_companies["Neuralink"]["funding"])

    with w2:
        company_card("Synchron", tracked_companies["Synchron"]["stage"], tracked_companies["Synchron"]["valuation"], funding=tracked_companies["Synchron"]["funding"])

    with w3:
        company_card("Paradromics", tracked_companies["Paradromics"]["stage"], tracked_companies["Paradromics"]["valuation"], funding=tracked_companies["Paradromics"]["funding"])

    with w4:
        company_card("Blackrock Neurotech", tracked_companies["Blackrock Neurotech"]["stage"], tracked_companies["Blackrock Neurotech"]["valuation"], funding=tracked_companies["Blackrock Neurotech"]["funding"])

    with w5:
        company_card("Precision Neuroscience", tracked_companies["Precision Neuroscience"]["stage"], tracked_companies["Precision Neuroscience"]["valuation"], funding=tracked_companies["Precision Neuroscience"]["funding"])'''

new = '''    watchlist_columns = st.columns(len(tracked_companies))

    for column, (company_name, company_data) in zip(watchlist_columns, tracked_companies.items()):
        with column:
            company_card(
                company_name,
                company_data["stage"],
                company_data["valuation"],
                funding=company_data["funding"],
            )'''

if old not in text:
    raise SystemExit("Could not find repeated Watchlist company_card block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 38 applied: Watchlist now renders from tracked_companies loop.")
