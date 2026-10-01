from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Fix dashboard card invisible routing overlay */
    div[data-testid="column"]:has(.veles-command-card) {
        position: relative;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton {
        position: relative;
        margin-top: -190px !important;
        height: 190px !important;
        z-index: 20;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button {
        height: 190px !important;
        min-height: 190px !important;
        width: 100% !important;
        opacity: 0 !important;
        border: 0 !important;
        background: transparent !important;
        cursor: pointer !important;
        padding: 0 !important;
        box-shadow: none !important;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button:hover,
    div[data-testid="column"]:has(.veles-command-card) .stButton > button:focus,
    div[data-testid="column"]:has(.veles-command-card) .stButton > button:active {
        opacity: 0 !important;
        border: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
    }
"""

if "/* Fix dashboard card invisible routing overlay */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Dashboard card routing overlay fixed.")
