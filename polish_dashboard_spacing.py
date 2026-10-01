from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Dashboard spacing polish */
    .veles-terminal-section-label {
        margin-top: 18px !important;
        margin-bottom: 12px !important;
    }

    .veles-terminal-metric {
        margin-bottom: 6px;
    }
"""

if "/* Dashboard spacing polish */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Dashboard spacing polished.")
