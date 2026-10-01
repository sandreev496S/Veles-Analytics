from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Final dashboard command card visual override */
    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button {
        min-height: 156px !important;
        height: 156px !important;
        display: flex !important;
        align-items: flex-start !important;
        justify-content: flex-start !important;
        text-align: left !important;
        white-space: pre-line !important;
        padding: 28px 30px !important;
        border-radius: 26px !important;
        color: #F8FAFC !important;
        background:
            radial-gradient(circle at 8% 10%, rgba(56,189,248,0.18), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.92), rgba(2,6,23,0.78)) !important;
        border: 1px solid rgba(148,163,184,0.20) !important;
        box-shadow:
            0 20px 48px rgba(0,0,0,0.28),
            inset 0 0 42px rgba(37,99,235,0.04) !important;
        font-size: 15px !important;
        font-weight: 850 !important;
        line-height: 1.75 !important;
        transition: all 180ms ease !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:hover {
        transform: translateY(-3px) !important;
        border-color: rgba(56,189,248,0.46) !important;
        background:
            radial-gradient(circle at 8% 10%, rgba(56,189,248,0.26), transparent 32%),
            linear-gradient(180deg, rgba(15,23,42,0.98), rgba(2,6,23,0.86)) !important;
        color: #F8FAFC !important;
        box-shadow:
            0 28px 68px rgba(0,0,0,0.36),
            0 0 52px rgba(37,99,235,0.16) !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:focus,
    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:active {
        color: #F8FAFC !important;
        border-color: rgba(56,189,248,0.46) !important;
        background:
            radial-gradient(circle at 8% 10%, rgba(56,189,248,0.24), transparent 32%),
            linear-gradient(180deg, rgba(15,23,42,0.98), rgba(2,6,23,0.86)) !important;
        box-shadow:
            0 24px 58px rgba(0,0,0,0.32),
            0 0 42px rgba(37,99,235,0.12) !important;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button p {
        text-align: left !important;
        margin: 0 !important;
        color: inherit !important;
    }
"""

if "/* Final dashboard command card visual override */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)

print("Fixed command button visuals.")
