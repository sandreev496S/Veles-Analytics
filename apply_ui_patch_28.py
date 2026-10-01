from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with valuation_tab:
        activity_item(
            "Valuation History",
            "Saved DCF, rNPV, and Monte Carlo models linked to this company will appear here.",
            "Models"
        )

        activity_item(
            "Next Step",
            "Connect saved valuation records to selected_company so this tab becomes dynamic.",
            "Planned"
        )'''

new = '''    with valuation_tab:
        try:
            valuation_records = list_valuations_supabase(
                user_id=get_current_user()["id"]
            )

            company_records = [
                record for record in valuation_records
                if selected_company.lower() in str(record.get("name", "")).lower()
            ]

            if company_records:
                valuation_df = pd.DataFrame(company_records)
                st.dataframe(valuation_df, use_container_width=True)
            else:
                activity_item(
                    "No Saved Models Yet",
                    f"No saved valuation models are currently linked to {selected_company}. Run a DCF or rNPV model and save it to populate this tab.",
                    "Models"
                )

        except Exception as e:
            log_exception("research_workspace_valuation_history", e)
            activity_item(
                "Valuation History Unavailable",
                "Could not load saved valuation models right now.",
                "Error"
            )'''

if old not in text:
    raise SystemExit("Could not find Valuation History tab block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 28 applied: Valuation History tab now loads saved models.")
