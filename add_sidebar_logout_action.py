from pathlib import Path

path = Path("components/ui/navigation.py")
text = path.read_text()

old = '''    st.sidebar.markdown(
        """
        <div class="veles-sidebar-user-card">
            <div class="veles-user-name">Steven Andreev</div>
            <div class="veles-user-role">Founder · Personal Workspace</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return selected_page
'''

new = '''    st.sidebar.markdown(
        """
        <div class="veles-sidebar-user-card">
            <div class="veles-user-name">Steven Andreev</div>
            <div class="veles-user-role">Founder · Personal Workspace</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.sidebar.button("Sign out", key="sidebar_logout", use_container_width=True):
        for key in ["user", "access_token", "refresh_token", "current_page"]:
            st.session_state.pop(key, None)
        st.rerun()

    return selected_page
'''

if old not in text:
    raise SystemExit("Could not find sidebar user card block. Paste the bottom of navigation.py if this fails.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Sidebar logout action added.")
