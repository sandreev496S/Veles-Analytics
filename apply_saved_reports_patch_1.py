from pathlib import Path

path = Path("app.py")
text = path.read_text()

start_marker = '''elif page == "Saved Reports":'''
end_marker = '''elif page == "Settings":'''

if start_marker not in text:
    raise SystemExit("Could not find Saved Reports block.")

if end_marker not in text:
    raise SystemExit("Could not find Settings marker.")

start = text.index(start_marker)
end = text.index(end_marker, start)

new_block = '''elif page == "Saved Reports":

    page_header(
        "Saved Reports",
        "Cloud-stored PDFs, Excel models, and signed report downloads."
    )

    try:
        reports = list_user_reports(get_current_user()["id"])

        if not reports:
            activity_item(
                "No Saved Reports Yet",
                "Save a PDF or Excel model to cloud storage to populate this page.",
                "Saved Reports"
            )
        else:
            reports_df = pd.DataFrame(reports)

            section_title(
                "Report Library",
                "Filter and open saved cloud reports."
            )

            companies = sorted(
                [
                    company
                    for company in reports_df["company_name"].dropna().unique().tolist()
                    if company
                ]
            )

            company_filter = st.selectbox(
                "Filter by company",
                ["All Companies"] + companies,
                key="saved_reports_company_filter",
            )

            if company_filter != "All Companies":
                filtered_reports = [
                    report for report in reports
                    if report.get("company_name") == company_filter
                ]
            else:
                filtered_reports = reports

            filtered_df = pd.DataFrame(filtered_reports)

            metric_col1, metric_col2, metric_col3 = st.columns(3)

            with metric_col1:
                metric_card("Saved Reports", len(filtered_reports), company_filter)

            with metric_col2:
                metric_card("Companies", len(companies), "Linked Reports")

            with metric_col3:
                storage_mb = (
                    filtered_df["file_size_bytes"].fillna(0).astype(int).sum() / (1024 * 1024)
                    if not filtered_df.empty and "file_size_bytes" in filtered_df.columns
                    else 0
                )
                metric_card("Storage", f"{storage_mb:.2f} MB", "Filtered Reports")

            st.dataframe(filtered_df, use_container_width=True)

            if filtered_reports:
                label_map = {
                    f"{row['file_name']} | {row.get('company_name') or 'Unlinked'} | {row['report_type']} | {row['created_at']}": row["storage_path"]
                    for row in filtered_reports
                }

                selected_label = st.selectbox(
                    "Open saved report",
                    list(label_map.keys()),
                    key="saved_reports_select",
                )

                if st.button("Create Signed Download Link", key="create_saved_report_signed_link"):
                    signed_url = create_signed_report_url(label_map[selected_label])

                    if signed_url:
                        st.success("Signed link created.")
                        st.write(signed_url)
                        st.link_button("Open Report", signed_url)
                    else:
                        st.error("Signed URL was empty.")

    except Exception as e:
        log_exception("saved_reports_page", e)
        st.error(safe_error_message())

'''

text = text[:start] + new_block + text[end:]

path.write_text(text)

print("Saved Reports page redesigned with company filtering.")
