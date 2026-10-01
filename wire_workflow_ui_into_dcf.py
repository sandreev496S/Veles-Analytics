from pathlib import Path

path = Path("components/dcf_wizard.py")
text = path.read_text()

old_import = '''from components.dcf_steps.results_step import render_results_step'''

new_import = '''from components.dcf_steps.results_step import render_results_step
from components.ui.workflow import render_workflow_progress, render_workflow_cards'''

if old_import not in text:
    raise SystemExit("Could not find results_step import.")

text = text.replace(old_import, new_import, 1)

old_block = '''    st.progress((step_index + 1) / len(wizard_steps))

    step_col1, step_col2, step_col3 = st.columns([1, 3, 1])'''

new_block = '''    render_workflow_progress(wizard_steps, step_index)
    render_workflow_cards(wizard_steps, step_index)

    step_col1, step_col2, step_col3 = st.columns([1, 3, 1])'''

if old_block not in text:
    raise SystemExit("Could not find old progress block.")

text = text.replace(old_block, new_block, 1)

path.write_text(text)

print("Workflow UI wired into DCF wizard.")
