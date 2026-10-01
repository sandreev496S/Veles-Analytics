from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with reports_tab:
        try:
            report_records = list_user_reports(
                get_current_user()["id"]
            )

            company_reports = [
                report for report in report_records
                if (
                    str(report.get("company_name", "")).lower() == selected_company.lower()
                    or selected_company.lower() in str(report.get("file_name", "")).lower()
                )
            ]

            if company_reports:
                reports_df = pd.DataFrame(company_reports)
                st.dataframe(reports_df, use_container_width=True)

                report_options = {
                    f"{report.get('file_name')} | {report.get('report_type')} | {report.get('created_at')}": report.get("storage_path")
                    for report in company_reports
                }

                selected_report = st.selectbox(
                    "Open company report",
                    list(report_options.keys()),
                    key=f"research_workspace_report_select_{selected_company}",
                )

                if st.button(
                    "Create Signed Report Link",
                    key=f"research_workspace_signed_link_{selected_company}",
                ):
                    signed_url = create_signed_report_url(
                        report_options[selected_report]
                    )

                    if signed_url:
                        st.success("Signed report link created.")
                        st.write(signed_url)
                        st.link_button("Open Report", signed_url)
                    else:
                        st.error("Could not create signed report link.")
            else:
                activity_item(
                    "No Saved Reports Yet",
                    f"No cloud reports are currently linked to {selected_company}. Generate and save a PDF or Excel model to populate this tab.",
                    "Reports"
                )

        except Exception as e:
            log_exception("research_workspace_reports", e)
            activity_item(
                "Reports Unavailable",
                "Could not load saved reports right now.",
                "Error"
            )
'''

new = '''    with reports_tab:
        section_title(
            "Report Library",
            "Cloud-stored reports, model exports, and signed report access."
        )

        try:
            report_records = list_user_reports(
                get_current_user()["id"]
            )

            company_reports = [
                report for report in report_records
                if (
                    str(report.get("company_name", "")).lower() == selected_company.lower()
                    or selected_company.lower() in str(report.get("file_name", "")).lower()
                )
            ]

            report_k1, report_k2, report_k3 = st.columns(3)

            with report_k1:
                metric_card("Linked Reports", len(company_reports), selected_company)

            with report_k2:
                metric_card("Formats", "PDF / Excel", "Supported")

            with report_k3:
                metric_card("Access", "Signed URLs", "Secure Links")

            reports_left, reports_right = st.columns([1.4, 1])

            with reports_left:
                if company_reports:
                    reports_df = pd.DataFrame(company_reports)
                    st.dataframe(reports_df, use_container_width=True)
                else:
                    activity_item(
                        "No Saved Reports Yet",
                        f"No cloud reports are currently linked to {selected_company}. Generate and save a PDF or Excel model to populate this tab.",
                        "Reports"
                    )

            with reports_right:
                activity_item(
                    "Latest Memo",
                    "AI investment memos and valuation reports linked to this company will appear in the report library.",
                    "Memo"
                )

                activity_item(
                    "Export Center",
                    "PDF reports, Excel models, and future board-style memos should be accessible from this company terminal.",
                    "Exports"
                )

                activity_item(
                    "Secure Access",
                    "Signed report links provide controlled temporary access to files stored in cloud storage.",
                    "Storage"
                )

                if company_reports:
                    report_options = {
                        f"{report.get('file_name')} | {report.get('report_type')} | {report.get('created_at')}": report.get("storage_path")
                        for report in company_reports
                    }

                    selected_report = st.selectbox(
                        "Open company report",
                        list(report_options.keys()),
                        key=f"research_workspace_report_select_{selected_company}",
                    )

                    if st.button(
                        "Create Signed Report Link",
                        key=f"research_workspace_signed_link_{selected_company}",
                    ):
                        signed_url = create_signed_report_url(
                            report_options[selected_report]
                        )

                        if signed_url:
                            st.success("Signed report link created.")
                            st.write(signed_url)
                            st.link_button("Open Report", signed_url)
                        else:
                            st.error("Could not create signed report link.")

        except Exception as e:
            log_exception("research_workspace_reports", e)
            activity_item(
                "Reports Unavailable",
                "Could not load saved reports right now.",
                "Error"
            )
'''

if old not in text:
    raise SystemExit("Could not find current reports tab block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Research Workspace reports tab redesigned.")
