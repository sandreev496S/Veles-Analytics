from pathlib import Path

path = Path("components/ui/navigation.py")
text = path.read_text()

old = '''                if st.sidebar.button(
                    label,
                    key=f"nav_{item_label}",
                    use_container_width=True,
                ):
                    selected_page = item_label'''

new = '''                if st.sidebar.button(
                    label,
                    key=f"nav_{item_label}",
                    use_container_width=True,
                ):
                    st.session_state["current_page"] = item_label
                    st.rerun()'''

if old not in text:
    raise SystemExit("Could not find sidebar nav button block.")

text = text.replace(old, new, 1)

path.write_text(text)
print("Sidebar active state now updates immediately on navigation click.")
