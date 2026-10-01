from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Compact DCF workflow */
    .veles-workflow-shell {
        padding: 16px 20px !important;
        border-radius: 18px !important;
        margin-bottom: 14px !important;
    }

    .veles-workflow-card {
        min-height: 88px !important;
        height: 88px !important;
        padding: 16px 18px !important;
        border-radius: 18px !important;
    }

    .veles-workflow-status {
        font-size: 13px !important;
        margin-bottom: 12px !important;
    }

    .veles-workflow-title {
        font-size: 13px !important;
        font-weight: 900 !important;
        letter-spacing: -0.01em !important;
    }

    .veles-step-breadcrumb {
        margin: 16px 0 22px 0;
        padding: 14px 18px;
        border-radius: 16px;
        border: 1px solid rgba(148,163,184,0.18);
        background: rgba(15,23,42,0.58);
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .veles-step-breadcrumb span {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 800;
    }

    .veles-step-breadcrumb strong {
        color: #F8FAFC;
        font-size: 16px;
        font-weight: 950;
        letter-spacing: -0.02em;
    }
"""

if "/* Compact DCF workflow */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Compact DCF workflow styles added.")
