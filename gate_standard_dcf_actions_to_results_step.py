from pathlib import Path

path = Path("app.py")
text = path.read_text()

replacements = {
    'if page == "Standard DCF" and "dcf_outputs" in st.session_state:':
    'if page == "Standard DCF" and "dcf_outputs" in st.session_state and st.session_state.get("dcf_step_index") == 4:',

    'if page == "Standard DCF" and "standard_dcf_outputs" in st.session_state:':
    'if page == "Standard DCF" and "standard_dcf_outputs" in st.session_state and st.session_state.get("dcf_step_index") == 4:',
}

for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f"Could not find block condition: {old}")
    text = text.replace(old, new)

path.write_text(text)
print("Standard DCF memo/save/cloud actions now render only on Step 5 Results.")
