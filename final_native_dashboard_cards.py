from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

text = text.replace("from urllib.parse import quote\n", "")

start = text.index("def render_command_card(")
end = text.index("\ndef render_analyst_command_center", start)

new_func = '''def render_command_card(title, subtitle, icon, target_page):
    label = f"{icon}\\n{title}\\n{subtitle}\\nOpen →"

    if st.button(
        label,
        key=f"dashboard_command_{target_page}",
        use_container_width=True,
    ):
        st.session_state["current_page"] = target_page
        st.rerun()

'''

text = text[:start] + new_func + text[end:]
path.write_text(text)

print("Dashboard command cards use native Streamlit routing.")
