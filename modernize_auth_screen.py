from pathlib import Path

path = Path("services/auth.py")
text = path.read_text()

old = '''def auth_ui():
    st.sidebar.markdown("---")

    if is_authenticated():
        user = get_current_user()
        st.sidebar.success(f"Logged in as {user.get('email')}")

        if st.sidebar.button("Logout", key="auth_logout_button"):
            st.session_state.pop("user", None)
            st.session_state.pop("access_token", None)
            st.rerun()

        return True

    st.sidebar.subheader("Account")

    mode = st.sidebar.radio(
        "Auth mode",
        ["Login", "Register"],
        horizontal=True
    )

    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")

    if mode == "Login":
        if st.sidebar.button("Login", key="auth_login_button"):
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
                    st.sidebar.error("Login failed.")

            except Exception as e:
                st.sidebar.error(f"Login failed: {e}")

    if mode == "Register":
        if st.sidebar.button("Create Account", key="auth_create_account_button"):
            try:
                response = supabase.auth.sign_up(
                    {
                        "email": email,
                        "password": password,
                    }
                )

                if response.user:
                    st.sidebar.success("Account created. Check your email if confirmation is required.")
                else:
                    st.sidebar.error("Registration failed.")

            except Exception as e:
                st.sidebar.error(f"Registration failed: {e}")

    return False
'''

new = '''def logout_button():
    if st.sidebar.button("Logout", key="auth_logout_button"):
        st.session_state.pop("user", None)
        st.session_state.pop("access_token", None)
        st.rerun()


def auth_ui():
    if is_authenticated():
        return True

    st.markdown(
        """
        <div class="veles-login-shell">
            <div class="veles-login-brand">◆ VELES ANALYTICS</div>
            <div class="veles-login-title">Institutional AI Research Platform</div>
            <div class="veles-login-subtitle">
                Sign in to access valuation models, company research, saved reports, and analyst workspaces.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    login_col, info_col = st.columns([1, 1])

    with login_col:
        st.markdown('<div class="veles-login-card">', unsafe_allow_html=True)

        mode = st.radio(
            "Account access",
            ["Login", "Register"],
            horizontal=True,
            key="auth_mode",
        )

        email = st.text_input("Email", key="auth_email")
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

        st.markdown("</div>", unsafe_allow_html=True)

    with info_col:
        st.markdown(
            """
            <div class="veles-login-info-card">
                <div class="veles-login-info-title">Built for serious research workflows</div>
                <ul>
                    <li>Company intelligence database</li>
                    <li>DCF and biotech rNPV models</li>
                    <li>AI investment memos</li>
                    <li>Saved reports and valuation history</li>
                    <li>Cloud-stored institutional outputs</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    return False
'''

if old not in text:
    raise SystemExit("Could not find old auth_ui block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Auth UI modernized.")
