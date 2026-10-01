from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

old = '''def render_command_card(title, subtitle, icon):
    html = f"""
    <div class="veles-command-card">
        <div class="veles-command-icon">{icon}</div>
        <div class="veles-command-title">{title}</div>
        <div class="veles-command-subtitle">{subtitle}</div>
    </div>
    """

    st.markdown(dedent(html), unsafe_allow_html=True)
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

    if st.button(
        f"Open {title}",
        key=f"dashboard_command_{target_page}",
        use_container_width=True,
    ):
        st.session_state["current_page"] = target_page
        st.rerun()
'''

if old not in text:
    raise SystemExit("Could not find render_command_card function.")

text = text.replace(old, new, 1)

replacements = {
    'render_command_card("Standard DCF", "Enterprise valuation workflow", "◌")':
    'render_command_card("Standard DCF", "Enterprise valuation workflow", "◌", "Standard DCF")',

    'render_command_card("Biotech rNPV", "Clinical asset valuation", "◍")':
    'render_command_card("Biotech rNPV", "Clinical asset valuation", "◍", "Biotech rNPV")',

    'render_command_card("Research Workspace", "Company intelligence terminal", "◉")':
    'render_command_card("Research Workspace", "Company intelligence terminal", "◉", "Research Workspace")',

    'render_command_card("Generate Report", "AI memo and exports", "▤")':
    'render_command_card("Generate Report", "AI memo and exports", "▤", "Saved Reports")',
}

for old_call, new_call in replacements.items():
    if old_call not in text:
        raise SystemExit(f"Could not find call: {old_call}")
    text = text.replace(old_call, new_call, 1)

path.write_text(text)

print("Dashboard command cards now route to pages.")
