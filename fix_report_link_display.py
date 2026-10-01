from pathlib import Path

path = Path("app.py")
text = path.read_text()

text = text.replace(
    '            st.write("DEBUG report records:", report_records)\n\n',
    '',
    1,
)

old = '''                    if signed_url:
                        st.success("Signed report link created.")
                        st.link_button("Open Report", signed_url)
                    else:
                        st.error("Could not create signed report link.")'''

new = '''                    if signed_url:
                        st.success("Signed report link created.")
                        st.write(signed_url)
                        st.link_button("Open Report", signed_url)
                    else:
                        st.error("Could not create signed report link.")'''

if old not in text:
    raise SystemExit("Could not find signed URL display block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Removed debug output and added visible signed URL.")
