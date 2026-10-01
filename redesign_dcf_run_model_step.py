from pathlib import Path

path = Path("components/dcf_wizard.py")
text = path.read_text()

old = '''    if selected_step == "4 · Run Model":
        section_title(
            "Step 4 — Run Model",
            "Generate scenario outputs, sensitivity analysis, comparables, charts, and exports."
        )

        glass_card(
            title="Ready to Generate Institutional Valuation",
            eyebrow="Run Model",
            body="Veles will validate company inputs, merge forecast and valuation assumptions, run downside/base/upside DCF cases, build sensitivity analysis, calculate reverse DCF implied growth, generate comparable valuation outputs, and prepare exports."
        )

    if selected_step == "4 · Run Model" and st.button(
        "Run DCF Analysis",
        type="primary",
        use_container_width=True,
        key="dcf_run_model_button",
    ):'''

new = '''    if selected_step == "4 · Run Model":
        section_title(
            "Step 4 — Valuation Engine",
            "Validate assumptions, generate scenario outputs, prepare sensitivity analysis, and stage exports."
        )

        engine_col, output_col = st.columns([1.35, 1])

        with engine_col:
            glass_card(
                title="Ready to Generate Institutional Valuation",
                eyebrow="Valuation Engine",
                body="Veles will validate company inputs, merge forecast and valuation assumptions, run downside/base/upside DCF cases, build sensitivity analysis, calculate reverse DCF implied growth, generate comparable valuation outputs, and prepare exports."
            )

        with output_col:
            glass_card(
                title="Outputs Prepared",
                eyebrow="Model Package",
                body="Scenario summary, base-case forecast, sensitivity matrix, reverse DCF implied growth, comparable valuation output, PDF report data, and Excel export data."
            )

        run_model = st.button(
            "Run DCF Analysis",
            type="primary",
            use_container_width=True,
            key="dcf_run_model_button",
        )
    else:
        run_model = False

    if selected_step == "4 · Run Model" and run_model:'''

if old not in text:
    raise SystemExit("Could not find current Step 4 Run Model block.")

text = text.replace(old, new, 1)
path.write_text(text)

print("DCF Run Model step redesigned.")
