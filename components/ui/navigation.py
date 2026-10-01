import streamlit as st


NAV_SECTIONS = [
    {
        "label": "Command",
        "items": [
            ("Dashboard", "⌂"),
            ("Clients", "▣"),
        ],
    },
    {
        "label": "Research",
        "items": [
            ("Companies", "◈"),
            ("Research Workspace", "◉"),
        ],
    },
    {
        "label": "Valuation",
        "items": [
            ("Standard DCF", "◌"),
            ("Biotech rNPV", "◍"),
        ],
    },
    {
        "label": "Library",
        "items": [
            ("Saved Models", "◫"),
            ("Saved Reports", "▤"),
        ],
    },
    {
        "label": "Platform",
        "items": [
            ("Settings", "⚙"),
            ("Methodology", "ⓘ"),
        ],
    },
]


def render_sidebar_navigation(current_page):
    st.sidebar.markdown(
        """
        <div class="veles-sidebar-brand">
            <div class="veles-sidebar-logo">◆ VELES</div>
            <div class="veles-sidebar-subtitle">Institutional AI Research Platform</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    selected_page = current_page

    for section in NAV_SECTIONS:
        st.sidebar.markdown(
            f'<div class="veles-nav-section-label">{section["label"]}</div>',
            unsafe_allow_html=True,
        )

        for item_label, icon in section["items"]:
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
                    st.session_state["current_page"] = item_label
                    st.rerun()

    st.sidebar.markdown(
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
