from pathlib import Path

path = Path("components/dcf_wizard.py")
text = path.read_text()

old = '''    render_workflow_progress(wizard_steps, step_index)
    render_workflow_cards(wizard_steps, step_index)

    step_col1, step_col2, step_col3 = st.columns([1, 3, 1])

    with step_col1:
        if step_index > 0:
            if st.button("← Back", key="dcf_back_button"):
                st.session_state["dcf_step_index"] -= 1
                st.rerun()

    with step_col2:
        st.markdown(
            f"""
            <div class="veles-card" style="text-align:center;">
                <div class="veles-metric-label">Step {step_index + 1} of {len(wizard_steps)}</div>
                <div class="veles-metric-value">{selected_step}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with step_col3:
        if step_index < len(wizard_steps) - 1:
            if st.button("Next →", key="dcf_next_button"):
                st.session_state["dcf_step_index"] += 1
                st.rerun()
'''

new = '''    nav_left, nav_center, nav_right = st.columns([1, 5, 1])

    with nav_left:
        if step_index > 0:
            if st.button("← Back", key="dcf_back_button", use_container_width=True):
                st.session_state["dcf_step_index"] -= 1
                st.rerun()

    with nav_center:
        render_workflow_progress(wizard_steps, step_index)

    with nav_right:
        if step_index < len(wizard_steps) - 1:
            if st.button("Next →", key="dcf_next_button", use_container_width=True):
                st.session_state["dcf_step_index"] += 1
                st.rerun()

    render_workflow_cards(wizard_steps, step_index)

    st.markdown(
        f"""
        <div class="veles-step-breadcrumb">
            <span>Step {step_index + 1} of {len(wizard_steps)}</span>
            <strong>{selected_step}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )
'''

if old not in text:
    raise SystemExit("Could not find DCF workflow navigation block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("DCF workflow header compacted.")
