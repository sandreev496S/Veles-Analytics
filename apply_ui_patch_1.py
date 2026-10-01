from pathlib import Path

path = Path("app.py")
text = path.read_text()

replacements = [
    (
        'st.sidebar.title("Veles DCF Analyst")',
        'st.sidebar.markdown("# Veles Analytics")',
    ),
    (
        '''page = st.sidebar.radio(
    "Navigation",
    [
        "Standard DCF",
        "Biotech rNPV",
        "Saved Valuations",
        "Saved Reports",
        "Methodology",
    ],
)''',
        '''page = st.sidebar.radio(
    "Workspace",
    [
        "Dashboard",
        "Standard DCF",
        "Biotech rNPV",
        "Saved Valuations",
        "Saved Reports",
        "Methodology",
    ],
)''',
    ),
    (
        '''st.title("Veles DCF Analyst")
st.caption("Professional discounted cash flow and biotech risk-adjusted valuation tools.")''',
        '''page_header(
    "Veles Analytics",
    "Institutional AI research platform for neurotechnology and biotech."
)''',
    ),
    (
        '''if page == "Standard DCF":''',
        '''if page == "Dashboard":

    page_header(
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

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Valuations", valuations_count, "Stored")

    with col2:
        metric_card("Reports", reports_count, "Generated")

    with col3:
        metric_card("Coverage", "5", "Neurotech")

    with col4:
        metric_card("Platform", "Online", "Healthy")

    st.markdown("##")

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

elif page == "Standard DCF":''',
    ),
]

for old, new in replacements:
    if old not in text:
        raise SystemExit(f"Could not find expected block:\n{old[:200]}")
    text = text.replace(old, new, 1)

path.write_text(text)
print("UI patch 1 applied successfully.")
