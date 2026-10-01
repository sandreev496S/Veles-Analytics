from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''st.sidebar.markdown("# Veles Analytics")

page = st.sidebar.radio(
    "Workspace",
    [
        "Dashboard",
        "Research Workspace",
        "Standard DCF",
        "Biotech rNPV",
        "Saved Models",
        "Saved Reports",
        "Settings",
        "Methodology",
    ],
)'''

new = '''st.sidebar.markdown("# Veles Analytics")

st.sidebar.markdown("### Command Center")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
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
st.sidebar.markdown("Models · Storage · Settings")'''

if old not in text:
    raise SystemExit("Could not find sidebar navigation block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("UI patch 21 applied: sidebar navigation grouped.")
