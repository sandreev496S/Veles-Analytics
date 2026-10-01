from pathlib import Path

path = Path("services/auth.py")
text = path.read_text()

start = text.index("def auth_ui():")
end = text.index("\ndef logout_button():", start) if "\ndef logout_button():" in text[start:] else len(text)

new_auth = '''def auth_ui():
    if is_authenticated():
        return True

    st.markdown(
        """
        <div class="veles-auth-page">
            <div class="veles-auth-bg-grid"></div>
            <div class="veles-auth-orb veles-auth-orb-left"></div>
            <div class="veles-auth-orb veles-auth-orb-right"></div>

            <div class="veles-auth-shell">
                <div class="veles-auth-hero">
                    <div class="veles-auth-kicker">◆ VELES ANALYTICS</div>
                    <div class="veles-auth-title">
                        Institutional AI research infrastructure for neurotechnology and biotech.
                    </div>
                    <div class="veles-auth-subtitle">
                        Build valuation models, generate investment memos, track company intelligence,
                        and store institutional reports inside a secure analyst workspace.
                    </div>

                    <div class="veles-auth-feature-grid">
                        <div class="veles-auth-feature">DCF Engine</div>
                        <div class="veles-auth-feature">Biotech rNPV</div>
                        <div class="veles-auth-feature">AI Memos</div>
                        <div class="veles-auth-feature">Research Workspace</div>
                        <div class="veles-auth-feature">Cloud Reports</div>
                        <div class="veles-auth-feature">Model Library</div>
                    </div>
                </div>

                <div class="veles-auth-card-wrap">
                    <div class="veles-auth-card-header">
                        <div class="veles-auth-logo-mark">⌁</div>
                        <div>
                            <div class="veles-auth-card-title">Welcome back</div>
                            <div class="veles-auth-card-caption">Access your Veles workspace</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _, form_col, _ = st.columns([1.25, 1, 1.25])

    with form_col:
        st.markdown('<div class="veles-auth-form-card">', unsafe_allow_html=True)

        mode = st.radio(
            "Account access",
            ["Login", "Register"],
            horizontal=True,
            key="auth_mode",
        )

        email = st.text_input("Email address", key="auth_email")
        password = st.text_input("Password", type="password", key="auth_password")

        if mode == "Login":
            if st.button("Sign In", key="auth_login_button", use_container_width=True):
                try:
                    response = supabase.auth.sign_in_with_password(
                        {
                            "email": email,
                            "password": password,
                        }
                    )

                    if response.user:
                        st.session_state["user"] = {
                            "id": response.user.id,
                            "email": response.user.email,
                        }

                        if response.session:
                            st.session_state["access_token"] = response.session.access_token

                        st.rerun()
                    else:
                        st.error("Login failed.")

                except Exception as e:
                    st.error(f"Login failed: {e}")

        if mode == "Register":
            if st.button("Create Account", key="auth_create_account_button", use_container_width=True):
                try:
                    response = supabase.auth.sign_up(
                        {
                            "email": email,
                            "password": password,
                        }
                    )

                    if response.user:
                        st.success("Account created. Check your email if confirmation is required.")
                    else:
                        st.error("Registration failed.")

                except Exception as e:
                    st.error(f"Registration failed: {e}")

        st.markdown(
            """
            <div class="veles-auth-footnote">
                Secure workspace for valuation, research, and report generation.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

    return False

'''

text = text[:start] + new_auth + text[end:]

if "def logout_button():" not in text:
    text += '''


def logout_button():
    if st.sidebar.button("Logout", key="sidebar_logout_button"):
        st.session_state.pop("user", None)
        st.session_state.pop("access_token", None)
        st.rerun()
'''

path.write_text(text)
print("Rebuilt fullscreen auth UI.")
