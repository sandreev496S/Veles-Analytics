from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with valuation_tab:
        try:
            valuation_records = list_valuations_supabase(
                user_id=get_current_user()["id"]
            )

            company_records = [
                record for record in valuation_records
                if (
                    str(record.get("company_name", "")).lower() == selected_company.lower()
                    or selected_company.lower() in str(record.get("name", "")).lower()
                )
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
            )
'''

new = '''    with valuation_tab:
        section_title(
            "Valuation Intelligence",
            "Saved models, linked valuation outputs, and export readiness."
        )

        try:
            valuation_records = list_valuations_supabase(
                user_id=get_current_user()["id"]
            )

            company_records = [
                record for record in valuation_records
                if (
                    str(record.get("company_name", "")).lower() == selected_company.lower()
                    or selected_company.lower() in str(record.get("name", "")).lower()
                )
            ]

            val_k1, val_k2, val_k3 = st.columns(3)

            with val_k1:
                metric_card("Linked Models", len(company_records), selected_company)

            with val_k2:
                metric_card("Model Types", "DCF / rNPV", "Supported")

            with val_k3:
                metric_card("Export Status", "Ready", "PDF / Excel")

            valuation_left, valuation_right = st.columns([1.4, 1])

            with valuation_left:
                if company_records:
                    valuation_df = pd.DataFrame(company_records)
                    st.dataframe(valuation_df, use_container_width=True)
                else:
                    activity_item(
                        "No Saved Models Yet",
                        f"No saved valuation models are currently linked to {selected_company}. Run a DCF or rNPV model and save it to populate this tab.",
                        "Models"
                    )

            with valuation_right:
                activity_item(
                    "Latest Valuation",
                    "Use saved DCF or rNPV outputs to build company-level valuation history and investment memo context.",
                    "Valuation"
                )

                activity_item(
                    "Scenario Analysis",
                    "Next step: surface downside, base case, upside, sensitivity, and implied growth outputs directly inside this company terminal.",
                    "Model Intelligence"
                )

                activity_item(
                    "Export Center",
                    "Reports and model exports should be accessible from this tab once linked to the company profile.",
                    "Reports"
                )

        except Exception as e:
            log_exception("research_workspace_valuation_history", e)
            activity_item(
                "Valuation History Unavailable",
                "Could not load saved valuation models right now.",
                "Error"
            )
'''

if old not in text:
    raise SystemExit("Could not find current valuation tab block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Research Workspace valuations tab redesigned.")
