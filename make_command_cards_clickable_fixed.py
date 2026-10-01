from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

# Replace function signature.
text = text.replace(
    "def render_command_card(title, subtitle, icon):",
    "def render_command_card(title, subtitle, icon, target_page):",
    1,
)

# Add open hint inside the card if not already present.
if "veles-command-open" not in text:
    text = text.replace(
        '''        <div class="veles-command-subtitle">{subtitle}</div>
    </div>''',
        '''        <div class="veles-command-subtitle">{subtitle}</div>
        <div class="veles-command-open">Open →</div>
    </div>''',
        1,
    )

# Add routing button after the card markdown call.
old = '''    st.markdown(dedent(html), unsafe_allow_html=True)


def render_analyst_command_center():'''

new = '''    st.markdown(dedent(html), unsafe_allow_html=True)

    if st.button(
        f"Open {title}",
        key=f"dashboard_command_{target_page}",
        use_container_width=True,
    ):
        st.session_state["current_page"] = target_page
        st.rerun()


def render_analyst_command_center():'''

if old not in text:
    raise SystemExit("Could not find insertion point after render_command_card markdown.")

text = text.replace(old, new, 1)

# Update calls.
call_replacements = {
    'render_command_card("Standard DCF", "Enterprise valuation workflow", "◌")':
    'render_command_card("Standard DCF", "Enterprise valuation workflow", "◌", "Standard DCF")',

    'render_command_card("Biotech rNPV", "Clinical asset valuation", "◍")':
    'render_command_card("Biotech rNPV", "Clinical asset valuation", "◍", "Biotech rNPV")',

    'render_command_card("Research Workspace", "Company intelligence terminal", "◉")':
    'render_command_card("Research Workspace", "Company intelligence terminal", "◉", "Research Workspace")',

    'render_command_card("Generate Report", "AI memo and exports", "▤")':
    'render_command_card("Generate Report", "AI memo and exports", "▤", "Saved Reports")',
}

for old_call, new_call in call_replacements.items():
    if old_call not in text:
        raise SystemExit(f"Could not find call: {old_call}")
    text = text.replace(old_call, new_call, 1)

path.write_text(text)
print("Dashboard command cards now route to pages.")
