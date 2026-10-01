from pathlib import Path

path = Path("components/ui/navigation.py")
text = path.read_text()

start = text.index('        for item_label, icon in section["items"]:')
end_marker = '''    st.sidebar.markdown(
        """
        <div class="veles-sidebar-user-card">'''

end = text.index(end_marker, start)

replacement = '''        for item_label, icon in section["items"]:
            label = f"{icon}  {item_label}"

            if item_label == current_page:
                st.sidebar.markdown(
                    f"""
                    <div class="veles-nav-current">
                        <span class="veles-nav-icon">{icon}</span>
                        <span>{item_label}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                if st.sidebar.button(
                    label,
                    key=f"nav_{item_label}",
                    use_container_width=True,
                ):
                    selected_page = item_label

'''

text = text[:start] + replacement + text[end:]

path.write_text(text)
print("Navigation click behavior fixed.")
