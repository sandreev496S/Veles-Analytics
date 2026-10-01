from pathlib import Path

path = Path("app.py")
text = path.read_text()

text = text.replace(
'''elif page == "Biotech rNPV":
    st.header("Biotech Risk-Adjusted NPV")
    st.caption("Probability-adjusted valuation for biotech, medtech, and neurotechnology assets.")

    with st.expander("Asset & Market Inputs", expanded=True):
        col1, col2, col3 = st.columns(3)''',
'''elif page == "Biotech rNPV":
    page_header(
        "Biotech rNPV Builder",
        "Institutional probability-adjusted valuation workflow for biotech, medtech, and neurotechnology assets."
    )

    section_title(
        "Asset & Market Assumptions",
        "Define the asset profile, market opportunity, clinical stage, launch timing, and probability of approval."
    )

    col1, col2, col3 = st.columns(3)''',
1
)

text = text.replace(
'''    with st.expander("Financial & Risk Inputs", expanded=True):
        col1, col2, col3 = st.columns(3)''',
'''    section_title(
        "Financial & Risk Assumptions",
        "Define discount rate, tax rate, R&D cost, launch cost, cash, debt, shares, and current market value."
    )

    col1, col2, col3 = st.columns(3)''',
1
)

path.write_text(text)
print("rNPV header and input sections redesigned.")
