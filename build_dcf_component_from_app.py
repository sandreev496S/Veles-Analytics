from pathlib import Path

app_path = Path("app.py")
component_path = Path("components/dcf_wizard.py")

app_text = app_path.read_text()

start_marker = 'elif page == "Standard DCF":'
end_marker = 'elif page == "Biotech rNPV":'

start = app_text.index(start_marker)
end = app_text.index(end_marker, start)

dcf_block = app_text[start:end]

# Remove top-level page condition and indent block into function body
dcf_body = dcf_block.replace(start_marker, "", 1)

# Remove exactly 4 leading spaces from non-empty lines, because the block was under elif
lines = dcf_body.splitlines()
normalized_lines = []
for line in lines:
    if line.startswith("    "):
        normalized_lines.append(line[4:])
    else:
        normalized_lines.append(line)
dcf_body = "\n".join(normalized_lines).strip("\n")

# Indent into function
indented_body = "\n".join(
    "    " + line if line.strip() else ""
    for line in dcf_body.splitlines()
)

component_text = '''import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from services.validation import ValidationError, validate_standard_dcf_inputs
from services.standard_dcf import (
    run_dcf_case,
    sensitivity_matrix,
    reverse_dcf_growth,
    comparable_valuation,
)
from services.pdf_report import create_dcf_pdf
from services.excel_export import create_standard_dcf_excel


def render_dcf_wizard(
    page_header,
    section_title,
    metric_card,
    activity_item,
):
''' + indented_body + "\n"

component_path.write_text(component_text)

print("Copied current Standard DCF block into components/dcf_wizard.py")
