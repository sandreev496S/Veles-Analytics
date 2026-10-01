from pathlib import Path

path = Path("app.py")
text = path.read_text()

anchor = "from components.ui.navigation import render_sidebar_navigation\n"
addition = "from components.ui.navigation import render_sidebar_navigation\nfrom components.ui.dashboard import render_research_terminal_header, render_analyst_command_center\n"

if anchor not in text:
    raise SystemExit("Could not find navigation import anchor.")

if "from components.ui.dashboard import render_research_terminal_header" not in text:
    text = text.replace(anchor, addition, 1)

old = '''    page_header(
        "Dashboard",
        "Research command center"
    )

    try:
        valuations_count = len(
            list_valuations_supabase(
                user_id=get_current_user()["id"]
            )
        )
    except Exception:
        valuations_count = 0

    try:
        reports_count = len(
            list_user_reports(
                get_current_user()["id"]
            )
        )
    except Exception:
        reports_count = 0

    section_title(
        "Platform Overview",
        "Your research, valuation, and report-generation command center."
    )

    tracked_companies = get_company_profiles()'''

new = '''    try:
        valuations_count = len(
            list_valuations_supabase(
                user_id=get_current_user()["id"]
            )
        )
    except Exception:
        valuations_count = 0

    try:
        reports_count = len(
            list_user_reports(
                get_current_user()["id"]
            )
        )
    except Exception:
        reports_count = 0

    tracked_companies = get_company_profiles()

    render_research_terminal_header(
        coverage_count=len(tracked_companies.keys()),
        valuations_count=valuations_count,
        reports_count=reports_count,
        notes_count=0,
    )

    render_analyst_command_center()

    section_title(
        "Platform Overview",
        "Operational metrics across valuation, reports, coverage, and system readiness."
    )'''

if old not in text:
    raise SystemExit("Could not find dashboard opening block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Dashboard terminal phase 1 wired.")
