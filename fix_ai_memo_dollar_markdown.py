from pathlib import Path

path = Path("app.py")
text = path.read_text()

text = text.replace(
    "        st.markdown(memo)",
    "        st.markdown(memo.replace('$', '\\\\$'))",
)

text = text.replace(
    "        st.markdown(biotech_memo)",
    "        st.markdown(biotech_memo.replace('$', '\\\\$'))",
)

path.write_text(text)

print("Escaped dollar signs before rendering AI memos in Markdown.")
