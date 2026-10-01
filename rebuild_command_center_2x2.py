from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

start = text.index("def render_command_card(")
end = text.index("\ndef render_analyst_command_center", start)

new_card_func = '''def render_command_card(title, subtitle, icon, target_page):
    label = f"{icon}\\n\\n{title}\\n{subtitle}\\n\\nOpen →"

    if st.button(
        label,
        key=f"dashboard_open_{target_page}",
        use_container_width=True,
    ):
        st.session_state["current_page"] = target_page
        st.rerun()

'''

text = text[:start] + new_card_func + text[end:]

start = text.index("def render_analyst_command_center():")
new_center_func = '''def render_analyst_command_center():
    st.markdown(
        '<div class="veles-terminal-section-label">Analyst Command Center</div>',
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
'''

text = text[:start] + new_center_func
path.write_text(text)

print("Rebuilt command center as 2x2 native clickable cards.")
