from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Equalize login card with hero */
    div[data-testid="column"]:has(.veles-auth-card-header-only) {
        margin-top: 95px;
    }
"""

if "/* Equalize login card with hero */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Login card position equalized.")
