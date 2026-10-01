# Technical Debt

## Current Priority Bugs

### DCF Wizard Step Rendering
Problem:
Step 2 forecast assumptions card appears on multiple wizard steps.

Fix:
Ensure each step only renders its own component:
- Step 1: company_step.py
- Step 2: forecast_step.py
- Step 3: scenarios_step.py
- Step 4: run_step.py
- Step 5: results_step.py

### AI Memo Formatting
Problem:
Dollar values and large numbers sometimes display poorly.

Fix:
Add formatting utilities:
- format_currency()
- format_millions()
- format_percent()
- format_multiple()

### Cleanup
Tasks:
- Remove old patch scripts after stable commits.
- Remove duplicate imports.
- Keep app.py thin.
- Keep wizard files modular.
