from pathlib import Path

path = Path("components/ui/navigation.py")
text = path.read_text()

old = '''        for item_label, icon in section["items"]:
            active_class = "veles-nav-item-active" if item_label == current_page else ""

            if st.sidebar.button(
                f"{icon}  {item_label}",
                key=f"nav_{item_label}",
                use_container_width=True,
            ):
                selected_page = item_label

            st.sidebar.markdown(
                f"""
                <script>
                </script>
                """,
                unsafe_allow_html=True,
            )'''

new = '''        for item_label, icon in section["items"]:
            active_class = "veles-nav-active-label" if item_label == current_page else "veles-nav-inactive-label"

            st.sidebar.markdown(
                f"""
                <div class="{active_class}">
                    <span class="veles-nav-icon">{icon}</span>
                    <span>{item_label}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.sidebar.button(
                "Open" if item_label != current_page else "Current",
                key=f"nav_{item_label}",
                use_container_width=True,
            ):
                selected_page = item_label'''

if old not in text:
    raise SystemExit("Could not find navigation item loop.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Navigation active labels added.")
