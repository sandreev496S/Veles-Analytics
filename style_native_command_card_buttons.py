from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Native dashboard command card buttons */
    div[data-testid="column"] .stButton > button {
        white-space: pre-line;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button,
    div[data-testid="column"] .stButton > button:has(p) {
        min-height: 150px;
        text-align: left;
        justify-content: flex-start;
        align-items: flex-start;
        padding: 22px 24px;
        border-radius: 24px;
        background:
            linear-gradient(180deg, rgba(15,23,42,0.84), rgba(15,23,42,0.58));
        border: 1px solid rgba(148,163,184,0.18);
        box-shadow: 0 18px 42px rgba(0,0,0,0.24);
        color: #F8FAFC;
        font-size: 16px;
        font-weight: 850;
        transition: all 160ms ease;
    }

    div[data-testid="column"]:has(button[id*="dashboard_open_"]) .stButton > button:hover,
    div[data-testid="column"] .stButton > button:has(p):hover {
        transform: translateY(-2px);
        border-color: rgba(56,189,248,0.34);
        box-shadow:
            0 24px 56px rgba(0,0,0,0.30),
            0 0 42px rgba(37,99,235,0.12);
        background:
            linear-gradient(180deg, rgba(15,23,42,0.95), rgba(15,23,42,0.68));
        color: #F8FAFC;
    }
"""

if "/* Native dashboard command card buttons */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Native command card buttons styled.")
