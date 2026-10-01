from pathlib import Path

path = Path("styles.py")
text = path.read_text()

insert_after = '''def status_pill(label, status="Neutral"):
    color = {
        "Positive": "#10B981",
        "Warning": "#F59E0B",
        "Danger": "#EF4444",
        "Neutral": "#3B82F6",
    }.get(status, "#3B82F6")

    st.markdown(f"""
    <span style="
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(59, 130, 246, 0.12);
        color: {color};
        border: 1px solid #1E293B;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.02em;
    ">
        {label}
    </span>
    """, unsafe_allow_html=True)
'''

addition = '''

def ai_workflow_card(title, steps):
    steps_html = ""

    for step in steps:
        steps_html += f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
            color: #E5E7EB;
            font-size: 14px;
        ">
            <span style="color: #10B981; font-weight: 800;">✓</span>
            <span>{step}</span>
        </div>
        """

    st.markdown(f"""
    <div class="veles-card">
        <div class="veles-insight-title">{title}</div>
        {steps_html}
    </div>
    """, unsafe_allow_html=True)
'''

if insert_after not in text:
    raise SystemExit("Could not find status_pill block in styles.py.")

text = text.replace(insert_after, insert_after + addition, 1)
path.write_text(text)

print("UI patch 14 applied successfully: ai_workflow_card added.")
