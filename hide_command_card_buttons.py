from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Hide dashboard command routing buttons while preserving click behavior */
    div[data-testid="column"]:has(.veles-command-card) .stButton > button {
        margin-top: -150px;
        min-height: 150px;
        height: 150px;
        opacity: 0;
        border: 0;
        background: transparent;
        cursor: pointer;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton {
        position: relative;
        z-index: 5;
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-card {
        transform: translateY(-2px);
        border-color: rgba(56,189,248,0.34);
        box-shadow:
            0 24px 56px rgba(0,0,0,0.30),
            0 0 42px rgba(37,99,235,0.12);
    }
"""

if "/* Hide dashboard command routing buttons while preserving click behavior */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)

print("Command card routing buttons hidden.")
