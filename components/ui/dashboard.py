import streamlit as st
from textwrap import dedent


def render_research_terminal_header(
    coverage_count,
    valuations_count,
    reports_count,
    notes_count=0,
):
    html = """
    <div class="veles-terminal-hero">
        <div class="veles-terminal-kicker">VELES ANALYTICS</div>
        <div class="veles-terminal-title">Institutional Research &amp; Valuation Platform</div>
        <div class="veles-terminal-subtitle">
            Neurotechnology, biotech, and frontier science intelligence terminal.
        </div>
    </div>
    """

    st.markdown(dedent(html), unsafe_allow_html=True)

    cols = st.columns(4)

    metrics = [
        ("Coverage Universe", coverage_count),
        ("Valuation Models", valuations_count),
        ("Research Notes", notes_count),
        ("Reports Generated", reports_count),
    ]

    for col, (label, value) in zip(cols, metrics):
        with col:
            st.markdown(
                dedent(
                    f"""
                    <div class="veles-terminal-metric">
                        <span>{label}</span>
                        <strong>{value}</strong>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )


def render_command_card(title, subtitle, icon, target_page):
    label = f"{icon}\n{title}\n{subtitle}\nOpen →"

    if st.button(
        label,
        key=f"dashboard_command_{target_page}",
        use_container_width=True,
    ):
        st.session_state["current_page"] = target_page
        st.rerun()


def render_analyst_command_center():
    st.markdown(
        '<div class="veles-command-center-scope"><div class="veles-terminal-section-label">Valuation & Research Console</div>',
        unsafe_allow_html=True,
    )

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        render_command_card(
            "Standard DCF",
            "Enterprise valuation workflow",
            "◌",
            "Standard DCF",
        )

    with row1_col2:
        render_command_card(
            "Biotech rNPV",
            "Clinical asset valuation",
            "◍",
            "Biotech rNPV",
        )

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        render_command_card(
            "Research Workspace",
            "Company intelligence terminal",
            "◉",
            "Research Workspace",
        )

    with row2_col2:
        render_command_card(
            "Generate Report",
            "AI memo and exports",
            "▤",
            "Saved Reports",
        )

    st.markdown("</div>", unsafe_allow_html=True)
