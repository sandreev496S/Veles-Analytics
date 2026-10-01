from pathlib import Path

path = Path("app.py")
text = path.read_text()

text = text.replace(
'''            with st.form("add_company_form"):
            col1, col2 = st.columns(2)''',
'''        with st.form("add_company_form"):
            col1, col2 = st.columns(2)''',
1
)

path.write_text(text)
print("Fixed Add Company form indentation.")
