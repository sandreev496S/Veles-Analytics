from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title(
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

new = '''    section_title(
        "Market Intelligence Terminal",
        "Funding signals, clinical milestones, regulatory events, and active coverage."
    )

    intelligence_col, coverage_col = st.columns([1.35, 1])

    with intelligence_col:
        st.markdown(
            '<div class="veles-mini-panel-title">Market Intelligence</div>',
            unsafe_allow_html=True,
        )

        activity_item(
            "Latest Funding Event",
            "Synchron remains a priority minimally invasive BCI company to monitor for future financing, clinical progress, and strategic investor activity.",
            "Funding Signal"
        )

        activity_item(
            "Latest Clinical Milestone",
            "Neuralink and other implantable BCI platforms should be tracked around human trial updates, safety outcomes, and device performance disclosures.",
            "Clinical Signal"
        )

        activity_item(
            "Latest Regulatory Event",
            "FDA progress, investigational device approvals, reimbursement positioning, and clinical trial expansion remain key valuation catalysts across the BCI universe.",
            "Regulatory Signal"
        )

        activity_item(
            "Priority Research Theme",
            "The strongest neurotechnology companies will combine clinical feasibility, durable data infrastructure, defensible hardware, and credible commercialization pathways.",
            "Research Lens"
        )

    with coverage_col:
        st.markdown(
            '<div class="veles-mini-panel-title">Coverage Universe</div>',
            unsafe_allow_html=True,
        )

        if tracked_companies:
            for company_name, company_data in list(tracked_companies.items())[:6]:
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
    raise SystemExit("Could not find current Research Intelligence block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Upgraded dashboard to Market Intelligence Terminal.")
