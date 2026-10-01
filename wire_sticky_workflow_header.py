from pathlib import Path

path = Path("components/dcf_wizard.py")
text = path.read_text()

old = '''    render_workflow_progress(wizard_steps, step_index)
    render_workflow_cards(wizard_steps, step_index)'''

new = '''    st.markdown('<div class="veles-sticky-workflow">', unsafe_allow_html=True)
    render_workflow_progress(wizard_steps, step_index)
    render_workflow_cards(wizard_steps, step_index)
    st.markdown('</div>', unsafe_allow_html=True)'''

if old not in text:
    raise SystemExit("Could not find workflow render block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("DCF workflow header is now sticky.")
