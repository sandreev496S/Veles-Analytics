from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''st.session_state.setdefault("current_page", "Dashboard")

if "nav" in st.query_params:
    nav_target = st.query_params.get("nav")

    if isinstance(nav_target, list):
        nav_target = nav_target[0]

    if nav_target:
        st.session_state["current_page"] = nav_target
        st.query_params.clear()

page = render_sidebar_navigation(st.session_state["current_page"])
st.session_state["current_page"] = page
'''

new = '''st.session_state.setdefault("current_page", "Dashboard")
page = render_sidebar_navigation(st.session_state["current_page"])
st.session_state["current_page"] = page
'''

if old in text:
    text = text.replace(old, new, 1)

path.write_text(text)
print("Query-param nav removed if present.")
