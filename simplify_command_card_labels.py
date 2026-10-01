from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

old = '''def render_command_card(title, subtitle, icon, target_page):
    label = f"{icon}\\n\\n{title}\\n{subtitle}\\n\\nOpen →"

    if st.button(
        label,
        key=f"dashboard_open_{target_page}",
        use_container_width=True,
    ):
        st.session_state["current_page"] = target_page
        st.rerun()
'''

new = '''def render_command_card(title, subtitle, icon, target_page):
    label = f"{icon}  {title}\\n{subtitle}\\nOpen →"

    if st.button(
        label,
        key=f"dashboard_open_{target_page}",
        use_container_width=True,
    ):
        st.session_state["current_page"] = target_page
        st.rerun()
'''

if old not in text:
    raise SystemExit("Could not find command card label block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Simplified command card labels.")
