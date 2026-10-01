from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Research Intelligence panel */
    .veles-mini-panel-title {
        color: #CBD5E1;
        font-size: 13px;
        font-weight: 900;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 2px 0 14px 2px;
    }
"""

if "/* Research Intelligence panel */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Research intelligence panel styles added.")
