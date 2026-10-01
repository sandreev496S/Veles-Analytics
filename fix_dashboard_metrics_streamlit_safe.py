from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

start = text.index("def render_research_terminal_header(")
end = text.index("\ndef render_command_card", start)

new_func = '''def render_research_terminal_header(
    coverage_count,
    valuations_count,
    reports_count,
    notes_count=0,
):
    html = """
    <div class="veles-terminal-hero">
        <div class="veles-terminal-kicker">VELES ANALYTICS</div>
        <div class="veles-terminal-title">Institutional Research &amp; Valuation Platform</div>
        <div class="veles-terminal-subtitle">
            Neurotechnology, biotech, and frontier science intelligence terminal.
        </div>
    </div>
    """

    st.markdown(dedent(html), unsafe_allow_html=True)

    cols = st.columns(4)

    metrics = [
        ("Coverage Universe", coverage_count),
        ("Valuation Models", valuations_count),
        ("Research Notes", notes_count),
        ("Reports Generated", reports_count),
    ]

    for col, (label, value) in zip(cols, metrics):
        with col:
            st.markdown(
                dedent(
                    f"""
                    <div class="veles-terminal-metric">
                        <span>{label}</span>
                        <strong>{value}</strong>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )

'''

text = text[:start] + new_func + text[end:]
path.write_text(text)

print("Dashboard terminal metrics now render Streamlit-safe.")
