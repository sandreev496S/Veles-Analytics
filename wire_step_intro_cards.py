from pathlib import Path

# Company step
path = Path("components/dcf_steps/company_step.py")
text = path.read_text()

if "from components.ui.cards import glass_card" not in text:
    text = text.replace("import streamlit as st\n", "import streamlit as st\nfrom components.ui.cards import glass_card\n", 1)

old = '''    section_title(
        "Step 1 — Company Information",
        "Enter the company profile and starting financial position."
    )

    col1, col2, col3 = st.columns(3)'''

new = '''    section_title(
        "Step 1 — Company Information",
        "Enter the company profile and starting financial position."
    )

    glass_card(
        title="Company Starting Point",
        eyebrow="Company",
        body="Enter the core financial position that anchors the valuation: market capitalization, net cash or debt, diluted shares, current revenue, and forecast horizon."
    )

    col1, col2, col3 = st.columns(3)'''

text = text.replace(old, new, 1)
path.write_text(text)

# Forecast step
path = Path("components/dcf_steps/forecast_step.py")
text = path.read_text()

if "from components.ui.cards import glass_card" not in text:
    text = text.replace("import streamlit as st\n", "import streamlit as st\nfrom components.ui.cards import glass_card\n", 1)

old = '''    scenarios = {}
    cols = st.columns(3)'''

new = '''    glass_card(
        title="Operating Forecast Assumptions",
        eyebrow="Forecast",
        body="Define revenue growth, operating margin, tax rate, depreciation and amortization, capital intensity, and working capital assumptions for each case."
    )

    scenarios = {}
    cols = st.columns(3)'''

text = text.replace(old, new, 1)
path.write_text(text)

# Scenarios step
path = Path("components/dcf_steps/scenarios_step.py")
text = path.read_text()

if "from components.ui.cards import glass_card" not in text:
    text = text.replace("import streamlit as st\n", "import streamlit as st\nfrom components.ui.cards import glass_card\n", 1)

old = '''    scenarios = {}
    cols = st.columns(3)'''

new = '''    glass_card(
        title="Valuation Scenario Assumptions",
        eyebrow="Scenarios",
        body="Set the valuation environment for each case: discount rate, terminal growth rate, and margin of safety. These assumptions drive terminal value and final implied share price."
    )

    scenarios = {}
    cols = st.columns(3)'''

text = text.replace(old, new, 1)
path.write_text(text)

print("Added intro glass cards to DCF steps 1-3.")
