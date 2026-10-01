from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''elif page == "Standard DCF":
    st.header("Standard DCF")

    with st.expander("Company & Financial Inputs", expanded=True):'''

new = '''elif page == "Standard DCF":

    page_header(
        "Standard DCF",
        "Guided intrinsic valuation workflow for public and private companies."
    )

    section_title(
        "Step 1 — Company Information",
        "Enter the company profile and starting financial position."
    )

    with st.expander("Company & Financial Inputs", expanded=True):'''

if old not in text:
    raise SystemExit("Could not find Standard DCF header block.")

text = text.replace(old, new, 1)

old2 = '''    st.subheader("Scenario Assumptions")'''

new2 = '''    section_title(
        "Step 2 — Forecast Assumptions",
        "Define downside, base, and upside case operating assumptions."
    )'''

if old2 not in text:
    raise SystemExit("Could not find Scenario Assumptions header.")

text = text.replace(old2, new2, 1)

old3 = '''    if st.button("Run DCF Analysis"):'''

new3 = '''    section_title(
        "Step 3 — Run Valuation",
        "Generate scenario outputs, sensitivity analysis, comparables, charts, and exports."
    )

    if st.button("Run DCF Analysis"):'''

if old3 not in text:
    raise SystemExit("Could not find Run DCF Analysis button.")

text = text.replace(old3, new3, 1)

path.write_text(text)
print("UI patch 9 applied successfully: Standard DCF page now has guided workflow headers.")
