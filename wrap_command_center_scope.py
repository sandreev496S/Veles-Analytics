from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

text = text.replace(
'''    st.markdown(
        '<div class="veles-terminal-section-label">Analyst Command Center</div>',
        unsafe_allow_html=True,
    )

    row1_col1, row1_col2 = st.columns(2)''',
'''    st.markdown(
        '<div class="veles-command-center-scope"><div class="veles-terminal-section-label">Analyst Command Center</div>',
        unsafe_allow_html=True,
    )

    row1_col1, row1_col2 = st.columns(2)''',
1
)

text = text.replace(
'''    with row2_col2:
        render_command_card(
            "Generate Report",
            "AI memo and exports",
            "▤",
            "Saved Reports",
        )
''',
'''    with row2_col2:
        render_command_card(
            "Generate Report",
            "AI memo and exports",
            "▤",
            "Saved Reports",
        )

    st.markdown("</div>", unsafe_allow_html=True)
''',
1
)

path.write_text(text)
print("Command center scoped.")
