from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Polished dashboard command launch cards */
    div[data-testid="column"] .stButton > button[kind="secondary"] {
        white-space: pre-line;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button {
        min-height: 168px;
        display: flex;
        align-items: flex-start;
        justify-content: flex-start;
        text-align: left;
        padding: 26px 24px;
        border-radius: 26px;
        color: #F8FAFC;
        background:
            radial-gradient(circle at 12% 12%, rgba(56,189,248,0.16), transparent 28%),
            linear-gradient(180deg, rgba(15,23,42,0.92), rgba(2,6,23,0.78));
        border: 1px solid rgba(148,163,184,0.20);
        box-shadow:
            0 18px 44px rgba(0,0,0,0.28),
            inset 0 0 38px rgba(37,99,235,0.04);
        font-size: 15px;
        font-weight: 850;
        line-height: 1.7;
        letter-spacing: -0.01em;
        transition: all 180ms ease;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button p {
        margin: 0;
        color: inherit;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:hover {
        transform: translateY(-3px);
        border-color: rgba(56,189,248,0.46);
        background:
            radial-gradient(circle at 12% 12%, rgba(56,189,248,0.24), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.98), rgba(2,6,23,0.84));
        box-shadow:
            0 26px 64px rgba(0,0,0,0.34),
            0 0 50px rgba(37,99,235,0.14);
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:active {
        transform: translateY(-1px);
    }
"""

if "/* Polished dashboard command launch cards */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Polished native command cards.")
