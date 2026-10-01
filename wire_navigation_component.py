from pathlib import Path

path = Path("app.py")
text = path.read_text()

# Add import
anchor = "from components.dcf_wizard import render_dcf_wizard\n"
new_anchor = "from components.dcf_wizard import render_dcf_wizard\nfrom components.ui.navigation import render_sidebar_navigation\n"

if anchor not in text:
    raise SystemExit("Could not find DCF wizard import anchor.")

if "from components.ui.navigation import render_sidebar_navigation" not in text:
    text = text.replace(anchor, new_anchor, 1)

old = '''st.sidebar.markdown("# Veles Analytics")

st.sidebar.markdown("### Command Center")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Companies",
        "Research Workspace",
        "Standard DCF",
        "Biotech rNPV",
        "Saved Models",
        "Saved Reports",
        "Settings",
        "Methodology",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("RESEARCH")
st.sidebar.markdown("Companies · Notes · Reports")

st.sidebar.caption("ANALYSIS")
st.sidebar.markdown("DCF · rNPV · Monte Carlo")

st.sidebar.caption("PLATFORM")
st.sidebar.markdown("Models · Storage · Settings")
'''

new = '''st.session_state.setdefault("current_page", "Dashboard")
page = render_sidebar_navigation(st.session_state["current_page"])
st.session_state["current_page"] = page
'''

if old not in text:
    raise SystemExit("Could not find old sidebar navigation block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("App now uses modern sidebar navigation component.")
