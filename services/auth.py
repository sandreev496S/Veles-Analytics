from __future__ import annotations

import streamlit as st
from dotenv import load_dotenv

from services.runtime_config import (
    AUTH_CONFIGURED,
    DEMO_MODE,
    SUPABASE_ANON_KEY,
    SUPABASE_URL,
)

load_dotenv()

_supabase = None
if AUTH_CONFIGURED:
    from supabase import create_client

    _supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def get_current_user():
    return st.session_state.get("user")


def is_authenticated():
    return get_current_user() is not None


def _activate_demo_user() -> bool:
    st.session_state.setdefault(
        "user",
        {"id": "demo-user", "email": "demo@veles.local"},
    )
    st.session_state.setdefault("access_token", "demo-token")
    return True


def auth_ui():
    if is_authenticated():
        return True

    if DEMO_MODE or not AUTH_CONFIGURED:
        st.info(
            "Veles is running in demo mode. Configure Supabase secrets and set "
            "APP_MODE=production to enable account authentication."
        )
        return _activate_demo_user()

    st.markdown(
        """
        <div class="veles-auth-background">
            <div class="veles-auth-bg-grid"></div>
            <div class="veles-auth-orb veles-auth-orb-left"></div>
            <div class="veles-auth-orb veles-auth-orb-right"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="veles-auth-spacer"></div>', unsafe_allow_html=True)

    hero_col, form_col = st.columns([1.2, 0.9], gap="large")
    with hero_col:
        st.markdown(
            """
            <div class="veles-auth-hero-panel">
                <div class="veles-auth-kicker">◆ VELES ANALYTICS</div>
                <div class="veles-auth-title">
                    Institutional AI research infrastructure for neurotechnology and biotech.
                </div>
                <div class="veles-auth-subtitle">
                    Build valuation models, generate investment memos, track company intelligence,
                    and store institutional reports inside a secure analyst workspace.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        feature_cols = st.columns(3)
        features = [
            "DCF Engine", "Biotech rNPV", "AI Memos",
            "Research Workspace", "Cloud Reports", "Model Library",
        ]
        for idx, feature in enumerate(features):
            with feature_cols[idx % 3]:
                st.markdown(
                    f'<div class="veles-auth-feature">{feature}</div>',
                    unsafe_allow_html=True,
                )

    with form_col:
        st.markdown(
            """
            <div class="veles-auth-card-header-only">
                <div class="veles-auth-logo-mark">⌁</div>
                <div>
                    <div class="veles-auth-card-title">Welcome back</div>
                    <div class="veles-auth-card-caption">Access your Veles workspace</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        mode = st.radio("Account access", ["Login", "Register"], horizontal=True, key="auth_mode")
        email = st.text_input("Email address", key="auth_email")
        password = st.text_input("Password", type="password", key="auth_password")

        if mode == "Login" and st.button("Sign In", key="auth_login_button", use_container_width=True):
            try:
                response = _supabase.auth.sign_in_with_password({"email": email, "password": password})
                if response.user:
                    st.session_state["user"] = {"id": response.user.id, "email": response.user.email}
                    if response.session:
                        st.session_state["access_token"] = response.session.access_token
                    st.rerun()
                st.error("Login failed.")
            except Exception as exc:
                st.error(f"Login failed: {exc}")

        if mode == "Register" and st.button("Create Account", key="auth_create_account_button", use_container_width=True):
            try:
                response = _supabase.auth.sign_up({"email": email, "password": password})
                if response.user:
                    st.success("Account created. Check your email if confirmation is required.")
                else:
                    st.error("Registration failed.")
            except Exception as exc:
                st.error(f"Registration failed: {exc}")

    return False


def logout_button():
    if st.sidebar.button("Logout", key="auth_logout_button"):
        st.session_state.pop("user", None)
        st.session_state.pop("access_token", None)
        st.rerun()
