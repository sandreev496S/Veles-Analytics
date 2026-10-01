from pathlib import Path

path = Path("app.py")
text = path.read_text()

text = text.replace('"Saved Valuations"', '"Saved Models"')
text = text.replace('elif page == "Saved Valuations":', 'elif page == "Saved Models":')
text = text.replace('st.header("Saved Valuations")', 'page_header("Saved Models", "Stored DCF, rNPV, and Monte Carlo valuation models.")')

path.write_text(text)
print("UI patch 7 applied successfully: Saved Valuations renamed to Saved Models.")
