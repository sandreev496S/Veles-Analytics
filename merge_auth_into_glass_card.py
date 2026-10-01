from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Auth glass card refinement */
    .veles-auth-card-header-only {
        background: rgba(15, 23, 42, 0.62);
        border: 1px solid rgba(148, 163, 184, 0.24);
        border-bottom: 0;
        border-radius: 30px 30px 0 0;
        padding: 32px 32px 16px 32px;
        box-shadow:
            0 28px 80px rgba(0,0,0,0.45),
            0 0 70px rgba(37,99,235,0.16);
        backdrop-filter: blur(24px);
        display: flex;
        gap: 18px;
        align-items: center;
    }

    .veles-auth-card-header-only + div {
        background: rgba(15, 23, 42, 0.62);
        border-left: 1px solid rgba(148, 163, 184, 0.24);
        border-right: 1px solid rgba(148, 163, 184, 0.24);
        border-bottom: 1px solid rgba(148, 163, 184, 0.24);
        border-radius: 0 0 30px 30px;
        padding: 12px 32px 32px 32px;
        backdrop-filter: blur(24px);
        box-shadow:
            0 28px 80px rgba(0,0,0,0.45),
            0 0 70px rgba(37,99,235,0.16);
    }

    .veles-auth-card-title {
        font-size: 34px;
        font-weight: 950;
        letter-spacing: -0.055em;
    }

    .veles-auth-card-caption {
        color: #94A3B8;
        font-size: 15px;
        margin-top: 4px;
    }

    .veles-auth-logo-mark {
        width: 62px;
        height: 62px;
        border-radius: 20px;
        font-size: 32px;
        background: linear-gradient(135deg, #2563EB, #06B6D4);
        box-shadow:
            0 18px 44px rgba(37,99,235,0.36),
            inset 0 0 18px rgba(255,255,255,0.16);
    }

    .veles-auth-spacer {
        height: 5vh;
    }
"""

if "/* Auth glass card refinement */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

# Neutralize older negative-margin form card if it still applies somewhere.
text = text.replace("margin-top: -330px;", "margin-top: 0;")
text = text.replace("padding: 150px 28px 28px 28px;", "padding: 28px;")

path.write_text(text)
print("Merged auth header and form into one glass card.")
