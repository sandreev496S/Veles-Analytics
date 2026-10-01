from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Auth card vertical alignment */
    div[data-testid="column"]:has(.veles-auth-card-header-only) {
        margin-top: 58px;
    }
"""

if "/* Auth card vertical alignment */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Lowered auth card slightly.")
