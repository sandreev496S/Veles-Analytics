import streamlit as st


def render_workflow_progress(steps, current_index):
    total = len(steps)
    progress = (current_index + 1) / total

    st.markdown(
        f"""
        <div class="veles-workflow-shell">
            <div class="veles-workflow-topline">
                <span>Valuation Workflow</span>
                <span>{current_index + 1} / {total}</span>
            </div>
            <div class="veles-workflow-progress-bg">
                <div class="veles-workflow-progress-fill" style="width: {progress * 100}%;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_workflow_cards(steps, current_index):
    cols = st.columns(len(steps))

    for idx, step in enumerate(steps):
        is_done = idx < current_index
        is_active = idx == current_index

        if is_done:
            status = "✓"
            state_class = "done"
        elif is_active:
            status = "●"
            state_class = "active"
        else:
            status = "○"
            state_class = "pending"

        with cols[idx]:
            st.markdown(
                f"""
                <div class="veles-workflow-card veles-workflow-card-{state_class}">
                    <div class="veles-workflow-status">{status}</div>
                    <div class="veles-workflow-title">{step}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
