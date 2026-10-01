from pathlib import Path

path = Path("app.py")
text = path.read_text()

start_marker = '''    company_profiles = {'''
end_marker = '''    }

    selected_company = st.selectbox('''

if start_marker not in text:
    raise SystemExit("Could not find company_profiles dictionary.")

start = text.index(start_marker)
end = text.index(end_marker, start) + len("    }\n\n")

replacement = '''    company_profiles = get_company_profiles()

'''

text = text[:start] + replacement + text[end:]

path.write_text(text)

print("Research Workspace now uses shared company profiles.")
