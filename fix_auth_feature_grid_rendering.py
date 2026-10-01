from pathlib import Path

path = Path("services/auth.py")
text = path.read_text()

old = '''                <div class="veles-auth-feature-grid">
                    <div class="veles-auth-feature">DCF Engine</div>
                    <div class="veles-auth-feature">Biotech rNPV</div>
                    <div class="veles-auth-feature">AI Memos</div>
                    <div class="veles-auth-feature">Research Workspace</div>
                    <div class="veles-auth-feature">Cloud Reports</div>
                    <div class="veles-auth-feature">Model Library</div>
                </div>'''

new = '''                <div class="veles-auth-feature-grid"></div>'''

if old not in text:
    raise SystemExit("Could not find raw feature grid block.")

text = text.replace(old, new, 1)

insert_after = '''            unsafe_allow_html=True,
        )

'''

feature_cards = '''        feature_cols = st.columns(3)

        features = [
            "DCF Engine",
            "Biotech rNPV",
            "AI Memos",
            "Research Workspace",
            "Cloud Reports",
            "Model Library",
        ]

        for idx, feature in enumerate(features):
            with feature_cols[idx % 3]:
                st.markdown(
                    f'<div class="veles-auth-feature">{feature}</div>',
                    unsafe_allow_html=True,
                )

'''

if "features = [" not in text:
    text = text.replace(insert_after, insert_after + feature_cards, 1)

path.write_text(text)

print("Feature grid now renders through Streamlit-safe columns.")
