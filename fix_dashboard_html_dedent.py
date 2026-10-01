from pathlib import Path

path = Path("components/ui/dashboard.py")
text = path.read_text()

if "from textwrap import dedent" not in text:
    text = text.replace("import streamlit as st\n", "import streamlit as st\nfrom textwrap import dedent\n", 1)

text = text.replace(
'''    st.markdown(
        f"""
        <div class="veles-terminal-hero">''',
'''    st.markdown(
        dedent(f"""
        <div class="veles-terminal-hero">''',
1
)

text = text.replace(
'''        """,
        unsafe_allow_html=True,
    )
    
    
def render_command_card''',
'''        """),
        unsafe_allow_html=True,
    )
    
    
def render_command_card''',
1
)

path.write_text(text)
print("Dashboard hero HTML now uses dedent.")
