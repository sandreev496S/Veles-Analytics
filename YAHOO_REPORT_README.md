# Veles Yahoo Report Rollback

This build keeps the current Streamlit application and PDF export fixes, but
restores the pre-validation equity-report assembler. Report metrics and
historical tables are read directly from the Yahoo Finance provider output.

## Run on macOS

```bash
cd ~/Downloads/veles_yahoo_report
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
VELES_DEMO_MODE=1 python -m streamlit run app.py
```

If the environment already exists, use only:

```bash
cd ~/Downloads/veles_yahoo_report
source .venv/bin/activate
VELES_DEMO_MODE=1 python -m streamlit run app.py
```

Yahoo can temporarily throttle or block requests. If a report is empty, close
the app, wait a few minutes, and retry; this rollback intentionally does not
substitute SEC facts for missing Yahoo values.
