from pathlib import Path

path = Path("styles.py")
text = path.read_text()

insert_after = '''def company_card(name, stage, valuation, sector="Brain-Computer Interface"):
    st.markdown(f"""
    <div class="veles-card">
        <div class="veles-company-name">{name}</div>
        <div class="veles-company-meta">{sector}</div>
        <div class="veles-company-meta">{stage}</div>
        <div class="veles-company-meta">{valuation}</div>
        <div class="veles-button-link">Open →</div>
    </div>
    """, unsafe_allow_html=True)
'''

addition = '''

def section_title(title, subtitle=None):
    subtitle_html = f'<div class="veles-page-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div style="margin-top: 18px; margin-bottom: 12px;">
        <div style="font-size: 22px; font-weight: 800; color: #F8FAFC;">{title}</div>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)


def activity_item(title, description, meta=""):
    meta_html = f'<div class="veles-company-meta">{meta}</div>' if meta else ""
    st.markdown(f"""
    <div class="veles-card">
        <div class="veles-company-name" style="font-size: 17px;">{title}</div>
        <div class="veles-insight-text" style="font-size: 14px;">{description}</div>
        {meta_html}
    </div>
    """, unsafe_allow_html=True)


def status_pill(label, status="Neutral"):
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

if insert_after not in text:
    raise SystemExit("Could not find company_card block in styles.py.")

text = text.replace(insert_after, insert_after + addition, 1)

path.write_text(text)
print("UI patch 4 applied successfully: section_title, activity_item, and status_pill added.")
