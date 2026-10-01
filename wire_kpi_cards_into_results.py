from pathlib import Path

path = Path("components/dcf_steps/results_step.py")
text = path.read_text()

old_import = '''import plotly.graph_objects as go

from services.pdf_report import create_dcf_pdf'''

new_import = '''import plotly.graph_objects as go

from components.ui.cards import kpi_card
from services.pdf_report import create_dcf_pdf'''

if old_import not in text:
    raise SystemExit("Could not find import anchor.")

text = text.replace(old_import, new_import, 1)

text = text.replace(
'''        with result_col1:
            metric_card(
                "Implied Share Price",
                f"${base_case['Implied Share Price ($)']:.2f}",
                "Base Case"
            )''',
'''        with result_col1:
            kpi_card(
                "Implied Share Price",
                f"${base_case['Implied Share Price ($)']:.2f}",
                "Base Case"
            )'''
)

text = text.replace(
'''        with result_col2:
            metric_card(
                "Equity Value",
                f"${base_case['Equity Value ($M)']:,.0f}M",
                "DCF Output"
            )''',
'''        with result_col2:
            kpi_card(
                "Equity Value",
                f"${base_case['Equity Value ($M)']:,.0f}M",
                "DCF Output"
            )'''
)

text = text.replace(
'''        with result_col3:
            metric_card(
                "Upside / Downside",
                f"{upside_pct:.1%}",
                "vs. Current Market Cap",
                positive=upside_pct >= 0
            )''',
'''        with result_col3:
            kpi_card(
                "Upside / Downside",
                f"{upside_pct:.1%}",
                "vs. Current Market Cap",
                positive=upside_pct >= 0
            )'''
)

text = text.replace(
'''        with result_col4:
            metric_card(
                "MoS Price",
                f"${base_case['MoS Price ($)']:.2f}",
                "Margin of Safety"
            )''',
'''        with result_col4:
            kpi_card(
                "MoS Price",
                f"${base_case['MoS Price ($)']:.2f}",
                "Margin of Safety"
            )'''
)

path.write_text(text)

print("DCF Results page now uses reusable KPI cards.")
