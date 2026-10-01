from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    page_header(
        "Companies",
        "Manage the company intelligence database used across Veles."
    )

    section_title(
        "Company Database",
        "Add, review, and manage tracked neurotechnology and biotech companies."
    )

    companies = list_companies()'''

new = '''    page_header(
        "Companies",
        "Manage the company intelligence database used across Veles."
    )

    companies = list_companies()

    st.markdown(
        f"""
        <div class="veles-company-terminal-hero">
            <div class="veles-company-terminal-kicker">Company Intelligence Database</div>
            <div class="veles-company-terminal-title">Coverage Universe</div>
            <div class="veles-company-terminal-subtitle">
                Tracked companies, technology modalities, funding profiles, and research workspace coverage.
            </div>
            <div class="veles-company-terminal-description">
                Maintain the core Veles company universe used across research workspaces, valuation models, reports, and AI-generated investment memos.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    stages = len(set([company.get("stage") for company in companies if company.get("stage")])) if companies else 0
    modalities = len(set([company.get("modality") for company in companies if company.get("modality")])) if companies else 0

    cov1, cov2, cov3, cov4 = st.columns(4)

    with cov1:
        metric_card("Tracked Companies", len(companies), "Coverage Universe")

    with cov2:
        metric_card("Stages", stages, "Company Maturity")

    with cov3:
        metric_card("Modalities", modalities, "Technology Types")

    with cov4:
        metric_card("Database", "Online", "Supabase")

    section_title(
        "Company Universe",
        "Review and manage tracked neurotechnology and biotech companies."
    )'''

if old not in text:
    raise SystemExit("Could not find Companies page opening block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Companies terminal hero added.")
