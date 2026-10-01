from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Final native dashboard command cards */
    div[data-testid="column"]:has(button[id*="dashboard_command_"]) .stButton > button {
        white-space: pre-line !important;
        min-height: 190px !important;
        height: 190px !important;
        width: 100% !important;
        display: flex !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
        text-align: left !important;
        padding: 28px 30px !important;
        border-radius: 28px !important;
        color: #F8FAFC !important;
        background:
            radial-gradient(circle at 10% 12%, rgba(56,189,248,0.20), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.96), rgba(2,6,23,0.82)) !important;
        border: 1px solid rgba(148,163,184,0.22) !important;
        box-shadow:
            0 22px 56px rgba(0,0,0,0.32),
            inset 0 0 42px rgba(37,99,235,0.05) !important;
        transition: all 180ms ease !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_command_"]) .stButton > button p {
        margin: 0 !important;
        text-align: left !important;
        color: inherit !important;
        font-size: 16px !important;
        font-weight: 850 !important;
        line-height: 1.75 !important;
        letter-spacing: -0.01em !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_command_"]) .stButton > button:hover {
        transform: translateY(-4px) !important;
        border-color: rgba(56,189,248,0.48) !important;
        color: #F8FAFC !important;
        background:
            radial-gradient(circle at 10% 12%, rgba(56,189,248,0.28), transparent 32%),
            linear-gradient(180deg, rgba(15,23,42,1), rgba(2,6,23,0.88)) !important;
        box-shadow:
            0 30px 74px rgba(0,0,0,0.38),
            0 0 58px rgba(37,99,235,0.18) !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_command_"]) .stButton > button:focus,
    div[data-testid="column"]:has(button[id*="dashboard_command_"]) .stButton > button:active {
        color: #F8FAFC !important;
        border-color: rgba(56,189,248,0.48) !important;
        box-shadow:
            0 24px 58px rgba(0,0,0,0.34),
            0 0 48px rgba(37,99,235,0.14) !important;
    }
"""

if "/* Final native dashboard command cards */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Final native command card styles added.")
