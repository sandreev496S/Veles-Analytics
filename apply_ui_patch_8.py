from pathlib import Path

path = Path("app.py")
text = path.read_text()

old_nav = '''        "Saved Models",
        "Saved Reports",
        "Methodology",'''

new_nav = '''        "Saved Models",
        "Saved Reports",
        "Settings",
        "Methodology",'''

if old_nav not in text:
    raise SystemExit("Could not find navigation block for Settings insertion.")

text = text.replace(old_nav, new_nav, 1)

old_block = '''elif page == "Methodology":'''

new_block = '''elif page == "Settings":

    page_header(
        "Settings",
        "Account, workspace, storage, and platform configuration."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        activity_item(
            "Account",
            "User profile, authentication state, and workspace access settings.",
            "Identity"
        )

    with col2:
        activity_item(
            "Storage",
            "Saved valuation models, PDFs, Excel exports, and cloud report usage.",
            "Files"
        )

    with col3:
        activity_item(
            "Billing",
            "Future Stripe subscription, usage limits, and invoice controls.",
            "Planned"
        )

    section_title(
        "Platform Controls",
        "Operational settings that will matter as Veles becomes an institutional product."
    )

    left, right = st.columns(2)

    with left:
        activity_item(
            "Security",
            "Audit logs, role-based permissions, rate limits, and session management will live here.",
            "Enterprise"
        )

        activity_item(
            "Data Sources",
            "Company database, research ingestion, documents, and external APIs.",
            "Research"
        )

    with right:
        activity_item(
            "Appearance",
            "Theme, density, table preferences, and analyst workspace layout.",
            "UI"
        )

        activity_item(
            "Notifications",
            "Report completion, valuation updates, watchlist alerts, and research events.",
            "Planned"
        )

elif page == "Methodology":'''

if old_block not in text:
    raise SystemExit("Could not find Methodology block.")

text = text.replace(old_block, new_block, 1)

path.write_text(text)
print("UI patch 8 applied successfully: Settings page added.")
