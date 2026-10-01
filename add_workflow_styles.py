from pathlib import Path

path = Path("styles.py")
text = path.read_text()

insert_before = "</style>"

css = """
    .veles-workflow-shell {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 22px;
        padding: 18px 20px;
        margin-bottom: 22px;
        box-shadow: 0 20px 45px rgba(0,0,0,0.22);
        backdrop-filter: blur(14px);
    }

    .veles-workflow-topline {
        display: flex;
        justify-content: space-between;
        color: #CBD5E1;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }

    .veles-workflow-progress-bg {
        height: 8px;
        width: 100%;
        border-radius: 999px;
        background: rgba(51, 65, 85, 0.9);
        overflow: hidden;
    }

    .veles-workflow-progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #2563EB, #06B6D4);
        transition: width 0.35s ease;
    }

    .veles-workflow-card {
        min-height: 92px;
        border-radius: 20px;
        padding: 18px;
        margin-bottom: 18px;
        border: 1px solid rgba(148, 163, 184, 0.18);
        background: rgba(15, 23, 42, 0.72);
        box-shadow: 0 12px 30px rgba(0,0,0,0.20);
        backdrop-filter: blur(12px);
    }

    .veles-workflow-card-active {
        border-color: rgba(59, 130, 246, 0.85);
        box-shadow: 0 0 0 1px rgba(59,130,246,0.35), 0 18px 45px rgba(37,99,235,0.20);
    }

    .veles-workflow-card-done {
        border-color: rgba(16, 185, 129, 0.5);
        background: rgba(6, 78, 59, 0.20);
    }

    .veles-workflow-card-pending {
        opacity: 0.68;
    }

    .veles-workflow-status {
        font-size: 20px;
        font-weight: 900;
        color: #38BDF8;
        margin-bottom: 8px;
    }

    .veles-workflow-title {
        color: #F8FAFC;
        font-size: 15px;
        font-weight: 800;
    }
"""

if css.strip() in text:
    print("Workflow styles already present.")
else:
    text = text.replace(insert_before, css + "\n    " + insert_before, 1)
    path.write_text(text)
    print("Workflow styles added.")
