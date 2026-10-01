from pathlib import Path

path = Path("app.py")
text = path.read_text()

start_marker = '''elif page == "Saved Models":'''
end_marker = '''elif page == "Saved Reports":'''

if start_marker not in text:
    raise SystemExit("Could not find Saved Models block.")

if end_marker not in text:
    raise SystemExit("Could not find Saved Reports marker.")

start = text.index(start_marker)
end = text.index(end_marker, start)

new_block = '''elif page == "Saved Models":

    page_header(
        "Saved Models",
        "Stored DCF, rNPV, and Monte Carlo valuation models."
    )

    records = list_valuations_supabase(user_id=get_current_user()["id"])

    if not records:
        activity_item(
            "No Saved Models Yet",
            "Run and save a DCF or biotech rNPV valuation to populate this page.",
            "Saved Models"
        )
    else:
        models_df = pd.DataFrame(records)

        section_title(
            "Model Library",
            "Filter and review saved valuation models."
        )

        companies = sorted(
            [
                company
                for company in models_df["company_name"].dropna().unique().tolist()
                if company
            ]
        )

        company_filter = st.selectbox(
            "Filter by company",
            ["All Companies"] + companies,
            key="saved_models_company_filter",
        )

        if company_filter != "All Companies":
            filtered_records = [
                record for record in records
                if record.get("company_name") == company_filter
            ]
        else:
            filtered_records = records

        filtered_df = pd.DataFrame(filtered_records)

        metric_col1, metric_col2, metric_col3 = st.columns(3)

        with metric_col1:
            metric_card("Saved Models", len(filtered_records), company_filter)

        with metric_col2:
            metric_card("Companies", len(companies), "Linked Models")

        with metric_col3:
            metric_card("Model Types", filtered_df["kind"].nunique() if not filtered_df.empty else 0, "Valuation Methods")

        st.dataframe(filtered_df, use_container_width=True)

        if filtered_records:
            label_map = {
                f"{row['name']} | {row.get('company_name') or 'Unlinked'} | {row['kind']} | {row['created_at']}": row["id"]
                for row in filtered_records
            }

            selected_label = st.selectbox(
                "Open saved model",
                list(label_map.keys()),
                key="saved_models_open_select",
            )

            selected_id = label_map[selected_label]

            if st.button("Load Saved Model", key="saved_models_load_button"):
                record = load_valuation_supabase(
                    selected_id,
                    user_id=get_current_user()["id"],
                )

                if record:
                    section_title(
                        record.get("name", "Saved Valuation"),
                        f"Type: {record.get('kind')} | Created: {record.get('created_at')}"
                    )

                    payload = record.get("payload", {})

                    for key, value in payload.items():
                        st.markdown(f"### {key.replace('_', ' ').title()}")

                        if isinstance(value, list):
                            try:
                                st.dataframe(pd.DataFrame(value), use_container_width=True)
                            except Exception:
                                st.json(value)
                        else:
                            st.json(value)
                else:
                    st.error("Could not load valuation.")

            section_title(
                "Delete Saved Model",
                "Remove a saved model from your workspace."
            )

            delete_label = st.selectbox(
                "Select model to delete",
                list(label_map.keys()),
                key="delete_saved_model_select",
            )

            delete_id = label_map[delete_label]

            confirm_delete_model = st.checkbox(
                "I understand this will delete the selected saved model.",
                key="confirm_delete_saved_model",
            )

            if st.button("Delete Selected Model", key="delete_saved_model_button"):
                if not confirm_delete_model:
                    st.error("Confirm deletion before continuing.")
                else:
                    deleted = delete_valuation_supabase(
                        delete_id,
                        user_id=get_current_user()["id"],
                    )

                    if deleted:
                        st.success(f"Deleted model: {delete_label}")
                        st.rerun()
                    else:
                        st.error("Could not delete model.")

'''

text = text[:start] + new_block + text[end:]

path.write_text(text)

print("Saved Models page redesigned with company filtering.")
