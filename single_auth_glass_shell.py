from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Final auth single-card shell */
    div[data-testid="column"]:has(.veles-auth-card-header-only) {
        background: rgba(15, 23, 42, 0.62);
        border: 1px solid rgba(148, 163, 184, 0.24);
        border-radius: 32px;
        padding: 34px 34px 32px 34px;
        box-shadow:
            0 30px 90px rgba(0,0,0,0.50),
            0 0 80px rgba(37,99,235,0.18);
        backdrop-filter: blur(26px);
    }

    .veles-auth-card-header-only {
        background: transparent;
        border: 0;
        border-radius: 0;
        padding: 0 0 24px 0;
        box-shadow: none;
        backdrop-filter: none;
        display: flex;
        gap: 18px;
        align-items: center;
        border-bottom: 1px solid rgba(148, 163, 184, 0.18);
        margin-bottom: 18px;
    }

    .veles-auth-card-header-only + div {
        background: transparent;
        border: 0;
        border-radius: 0;
        padding: 0;
        backdrop-filter: none;
        box-shadow: none;
    }
"""

if "/* Final auth single-card shell */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Added final single glass auth shell.")
