from pathlib import Path

path = Path("app.py")
text = path.read_text()

start_marker = 'elif page == "Standard DCF":'
end_marker = 'elif page == "Biotech rNPV":'

start = text.index(start_marker)
end = text.index(end_marker, start)

replacement = '''elif page == "Standard DCF":
    render_dcf_wizard(
        page_header=page_header,
        section_title=section_title,
        metric_card=metric_card,
        activity_item=activity_item,
    )

'''

text = text[:start] + replacement + text[end:]

path.write_text(text)

print("Replaced Standard DCF block with render_dcf_wizard call.")
