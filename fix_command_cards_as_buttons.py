from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

start = text.index("def render_command_card(")
end = text.index("\ndef render_analyst_command_center", start)

new_func = '''def render_command_card(title, subtitle, icon, target_page):
    if st.button(
        f"{icon}  {title}\\n\\n{subtitle}\\n\\nOpen →",
        key=f"dashboard_open_{target_page}",
        use_container_width=True,
    ):
        st.session_state["current_page"] = target_page
        st.rerun()

'''

text = text[:start] + new_func + text[end:]
path.write_text(text)

print("Command cards are now native routing buttons.")
