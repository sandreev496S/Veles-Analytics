from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

if "from urllib.parse import quote" not in text:
    text = text.replace(
        "from textwrap import dedent\n",
        "from textwrap import dedent\nfrom urllib.parse import quote\n",
        1,
    )

start = text.index("def render_command_card(")
end = text.index("\ndef render_analyst_command_center", start)

new_func = '''def render_command_card(title, subtitle, icon, target_page):
    nav_target = quote(target_page)

    html = f"""
    <a class="veles-command-link" href="?nav={nav_target}" target="_self">
        <div class="veles-command-card">
            <div class="veles-command-topline">
                <div class="veles-command-icon">{icon}</div>
                <div class="veles-command-arrow">→</div>
            </div>
            <div class="veles-command-title">{title}</div>
            <div class="veles-command-subtitle">{subtitle}</div>
        </div>
    </a>
    """

    st.markdown(dedent(html), unsafe_allow_html=True)

'''

text = text[:start] + new_func + text[end:]
path.write_text(text)

print("Command cards converted to real navigation links.")
