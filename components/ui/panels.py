import streamlit as st


def section_panel(title, subtitle=None):
    subtitle_html = f'<div class="veles-panel-subtitle">{subtitle}</div>' if subtitle else ""

    st.markdown(
        f"""
        <div class="veles-panel-header">
            <div class="veles-panel-title">{title}</div>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
