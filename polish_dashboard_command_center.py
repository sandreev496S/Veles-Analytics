from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Dashboard Sprint 2: elegant clickable command cards */
    .veles-terminal-hero {
        padding: 28px 36px !important;
        margin-bottom: 22px !important;
    }

    .veles-terminal-title {
        font-size: 34px !important;
        margin-bottom: 6px !important;
    }

    .veles-terminal-subtitle {
        margin-bottom: 0 !important;
    }

    .veles-terminal-section-label {
        margin-top: 24px !important;
        margin-bottom: 14px !important;
    }

    div[data-testid="column"]:has(button[kind="secondary"]) .stButton > button {
        white-space: pre-line;
        min-height: 190px;
        width: 100%;
        display: flex;
        align-items: flex-start;
        justify-content: flex-start;
        text-align: left;
        padding: 26px 28px;
        border-radius: 28px;
        color: #F8FAFC;
        background:
            radial-gradient(circle at 8% 12%, rgba(56,189,248,0.18), transparent 28%),
            linear-gradient(180deg, rgba(15,23,42,0.92), rgba(2,6,23,0.78));
        border: 1px solid rgba(148,163,184,0.20);
        box-shadow:
            0 20px 48px rgba(0,0,0,0.28),
            inset 0 0 42px rgba(37,99,235,0.04);
        transition: all 180ms ease;
    }

    div[data-testid="column"]:has(button[kind="secondary"]) .stButton > button p {
        width: 100%;
        margin: 0;
        color: inherit;
        font-size: 16px;
        font-weight: 850;
        line-height: 1.65;
        letter-spacing: -0.01em;
        text-align: left;
    }

    div[data-testid="column"]:has(button[kind="secondary"]) .stButton > button:hover {
        transform: translateY(-4px);
        border-color: rgba(56,189,248,0.46);
        background:
            radial-gradient(circle at 8% 12%, rgba(56,189,248,0.26), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.98), rgba(2,6,23,0.86));
        box-shadow:
            0 28px 68px rgba(0,0,0,0.36),
            0 0 52px rgba(37,99,235,0.16);
        color: #F8FAFC;
    }

    div[data-testid="column"]:has(button[kind="secondary"]) .stButton > button:active {
        transform: translateY(-1px);
    }
"""

if "/* Dashboard Sprint 2: elegant clickable command cards */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Polished dashboard command center cards and compact hero.")
