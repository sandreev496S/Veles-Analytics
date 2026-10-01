from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Dashboard command card routing buttons */
    .veles-command-open {
        margin-top: 18px;
        color: #38BDF8;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button {
        margin-top: -8px;
        border-radius: 16px;
        border: 1px solid rgba(56,189,248,0.20);
        background: rgba(2,6,23,0.38);
        color: #CBD5E1;
        font-size: 12px;
        font-weight: 850;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        transition: all 160ms ease;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button:hover {
        background: rgba(37,99,235,0.18);
        border-color: rgba(56,189,248,0.42);
        color: #F8FAFC;
        transform: translateY(-1px);
    }
"""

if "/* Dashboard command card routing buttons */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Command card buttons styled.")
