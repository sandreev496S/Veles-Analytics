from pathlib import Path

path = Path("styles.py")
text = path.read_text()

start = text.index("def company_card(")
next_def = text.find("\ndef ", start + 1)
end = next_def if next_def != -1 else len(text)

new_block = '''def company_card(name, stage, valuation, sector="Brain-Computer Interface", funding=None):
    if funding:
        body = f"""
        <div class="veles-card">
            <div class="veles-company-name">{name}</div>
            <div class="veles-company-meta">{sector}</div>
            <div class="veles-company-meta">{stage}</div>
            <div class="veles-company-meta">Funding: {funding}</div>
            <div class="veles-company-meta">Valuation: {valuation}</div>
            <div class="veles-button-link">Open →</div>
        </div>
        """
    else:
        body = f"""
        <div class="veles-card">
            <div class="veles-company-name">{name}</div>
            <div class="veles-company-meta">{sector}</div>
            <div class="veles-company-meta">{stage}</div>
            <div class="veles-company-meta">Valuation: {valuation}</div>
            <div class="veles-button-link">Open →</div>
        </div>
        """

    st.markdown(body, unsafe_allow_html=True)
'''

text = text[:start] + new_block + text[end:]
path.write_text(text)

print("Replaced company_card with simple non-nested HTML version.")
