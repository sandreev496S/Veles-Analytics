from pathlib import Path

path = Path("app.py")
text = path.read_text()

text = text.replace(
    "from services.auth import auth_ui, is_authenticated, get_current_user",
    "from services.auth import auth_ui, is_authenticated, get_current_user, logout_button",
    1,
)

old = '''load_veles_design_system()
st.session_state.setdefault("current_page", "Dashboard")
page = render_sidebar_navigation(st.session_state["current_page"])
st.session_state["current_page"] = page

page_header(
    "Veles Analytics",
    "Institutional AI research platform for neurotechnology and biotech."
)

authenticated = auth_ui()


if not authenticated:
    st.warning("Please log in or create an account to access Veles DCF Analyst.")
    st.stop()
'''

new = '''load_veles_design_system()

authenticated = auth_ui()

if not authenticated:
    st.stop()

st.session_state.setdefault("current_page", "Dashboard")
page = render_sidebar_navigation(st.session_state["current_page"])
st.session_state["current_page"] = page
logout_button()

page_header(
    "Veles Analytics",
    "Institutional AI research platform for neurotechnology and biotech."
)
'''

if old not in text:
    raise SystemExit("Could not find app auth/navigation block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Auth now renders before app shell.")
