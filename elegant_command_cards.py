from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

start = text.index("def render_command_card(")
end = text.index("\ndef render_analyst_command_center", start)

new_func = '''def render_command_card(title, subtitle, icon, target_page):
    html = f"""
    <div class="veles-command-card">
        <div class="veles-command-topline">
            <div class="veles-command-icon">{icon}</div>
            <div class="veles-command-arrow">→</div>
        </div>
        <div class="veles-command-title">{title}</div>
        <div class="veles-command-subtitle">{subtitle}</div>
    </div>
    """

    st.markdown(dedent(html), unsafe_allow_html=True)

    if st.button(
        "Open",
        key=f"dashboard_open_{target_page}",
        use_container_width=True,
    ):
        st.session_state["current_page"] = target_page
        st.rerun()

'''

text = text[:start] + new_func + text[end:]
path.write_text(text)

print("Command cards restored to elegant HTML cards with routing buttons.")
