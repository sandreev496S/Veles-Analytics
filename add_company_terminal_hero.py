from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = '''    section_title(
        selected_company,
        "Unified research profile"
    )'''

new = '''    st.markdown(
        f"""
        <div class="veles-company-terminal-hero">
            <div class="veles-company-terminal-kicker">Company Terminal</div>
            <div class="veles-company-terminal-title">{selected_company}</div>
            <div class="veles-company-terminal-subtitle">
                {selected_profile["stage"]} · {selected_profile["modality"]} · {selected_profile["valuation"]}
            </div>
            <div class="veles-company-terminal-description">
                Unified intelligence workspace for company profile, technology, funding, competition, valuations, notes, and reports.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )'''

if old not in text:
    raise SystemExit("Could not find selected company section_title block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Company terminal hero added.")
