from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title("AI Research Brief", "High-level platform intelligence and market context.")

    left, right = st.columns([2, 1])

    with left:
        insight_card(
            "AI Insight",
            "Brain-computer interface investment activity remains concentrated around Neuralink, Synchron, Paradromics, Precision Neuroscience, and Blackrock Neurotech."
        )

    with right:
        company_card(
            "Neuralink",
            "Series D",
            "$6.1B valuation"
        )

    section_title("Watchlist", "Priority neurotechnology companies under active coverage.")

    if tracked_companies:
        watchlist_columns = st.columns(len(tracked_companies))

        for column, (company_name, company_data) in zip(watchlist_columns, tracked_companies.items()):
            with column:
                company_card(
                    company_name,
                    company_data["stage"],
                    company_data["valuation"],
                    funding=company_data["funding"],
                )
    else:
        activity_item(
            "No Companies Found",
            "Seed the companies table in Supabase to populate the Dashboard watchlist.",
            "Company Database"
        )
'''

new = '''    section_title(
        "Research Intelligence",
        "Coverage universe, recent research, and priority company intelligence."
    )

    intelligence_col, coverage_col = st.columns([1.4, 1])

    with intelligence_col:
        insight_card(
            "Market Intelligence",
            "Brain-computer interface investment activity remains concentrated around invasive and minimally invasive platforms, with investor attention centered on Neuralink, Synchron, Paradromics, Precision Neuroscience, and Blackrock Neurotech."
        )

        activity_item(
            "Priority Theme",
            "Neurotechnology valuation depends on clinical progress, regulatory timing, device adoption, reimbursement pathways, and defensibility of neural data infrastructure.",
            "Research Lens"
        )

    with coverage_col:
        if tracked_companies:
            st.markdown(
                '<div class="veles-mini-panel-title">Coverage Universe</div>',
                unsafe_allow_html=True,
            )

            for company_name, company_data in list(tracked_companies.items())[:5]:
                activity_item(
                    company_name,
                    f'{company_data["stage"]} · {company_data["valuation"]}',
                    company_data["funding"],
                )
        else:
            activity_item(
                "No Companies Found",
                "Seed the companies table in Supabase to populate the Dashboard coverage universe.",
                "Company Database"
            )
'''

if old not in text:
    raise SystemExit("Could not find old AI Research Brief / Watchlist block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Dashboard Research Intelligence section replaced.")
