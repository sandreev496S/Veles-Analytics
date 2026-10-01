from pathlib import Path

path = Path("app.py")
text = path.read_text()

start_marker = '''load_veles_design_system()
st.markdown(
    """
    <style>'''

end_marker = '''    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("# Veles Analytics")'''

if start_marker not in text:
    raise SystemExit("Could not find old CSS block start. It may already be removed.")

if end_marker not in text:
    raise SystemExit("Could not find old CSS block end.")

start = text.index(start_marker)
end = text.index(end_marker) + len('''    """,
    unsafe_allow_html=True,
)

''')

replacement = '''load_veles_design_system()
'''

text = text[:start] + replacement + text[end:]

path.write_text(text)
print("UI patch 2 applied successfully: old CSS override removed.")
