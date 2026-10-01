import streamlit as st


def glass_card(title, body=None, eyebrow=None):
    eyebrow_html = f'<div class="veles-card-eyebrow">{eyebrow}</div>' if eyebrow else ""
    body_html = f'<div class="veles-card-body">{body}</div>' if body else ""

    st.markdown(
        f"""
        <div class="veles-glass-card">
            {eyebrow_html}
            <div class="veles-card-title">{title}</div>
            {body_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label, value, caption=None, positive=True):
    caption_class = "veles-kpi-positive" if positive else "veles-kpi-negative"
    caption_html = f'<div class="{caption_class}">{caption}</div>' if caption else ""

    st.markdown(
        f"""
        <div class="veles-kpi-card">
            <div class="veles-kpi-label">{label}</div>
            <div class="veles-kpi-value">{value}</div>
            {caption_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
