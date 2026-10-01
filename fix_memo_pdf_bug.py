from pathlib import Path

path = Path("app.py")
text = path.read_text()

old = 'st.session_state["standard_dcf_outputs"]["pdf"] = pdf'
new = 'st.session_state["standard_dcf_outputs"]["pdf"] = memo_pdf'

if old not in text:
    raise SystemExit("Could not find the undefined pdf assignment.")

text = text.replace(old, new, 1)
path.write_text(text)

print("Fixed memo PDF assignment bug.")
