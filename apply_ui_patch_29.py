from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    with reports_tab:
        activity_item(
            "Reports",
            "Generated PDFs, Excel models, and AI investment memos linked to this company will appear here.",
            "Exports"
        )'''

new = '''    with reports_tab:
        try:
            report_records = list_user_reports(
                get_current_user()["id"]
            )

            company_reports = [
                report for report in report_records
                if selected_company.lower() in str(report.get("file_name", "")).lower()
            ]

            if company_reports:
                reports_df = pd.DataFrame(company_reports)
                st.dataframe(reports_df, use_container_width=True)
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
            )'''

if old not in text:
    raise SystemExit("Could not find Reports tab block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 29 applied: Reports tab now loads saved cloud reports.")
