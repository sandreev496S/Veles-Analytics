from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

old = '''def render_command_card(title, subtitle, icon, target_page):
    html = f"""
    <div class="veles-command-card">
        <div class="veles-command-icon">{icon}</div>
        <div class="veles-command-title">{title}</div>
        <div class="veles-command-subtitle">{subtitle}</div>
        <div class="veles-command-open">Open →</div>
    </div>
    """

    st.markdown(dedent(html), unsafe_allow_html=True)

    if st.button(f"Open {title}", key=f"dashboard_open_{target_page}", use_container_width=True):
        st.session_state["current_page"] = target_page
        st.rerun()
'''

new = '''def render_command_card(title, subtitle, icon, target_page):
    html = f"""
    <div class="veles-command-card">
        <div class="veles-command-icon">{icon}</div>
        <div class="veles-command-title">{title}</div>
        <div class="veles-command-subtitle">{subtitle}</div>
        <div class="veles-command-open">Open →</div>
    </div>
    """

    st.markdown(dedent(html), unsafe_allow_html=True)

    # Invisible routing button: makes the card area feel clickable without showing a second button.
    if st.button(
        "",
        key=f"dashboard_open_{target_page}",
        use_container_width=True,
    ):
        st.session_state["current_page"] = target_page
        st.rerun()
'''

if old not in text:
    raise SystemExit("Could not find current render_command_card block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Command cards route without visible lower buttons.")
