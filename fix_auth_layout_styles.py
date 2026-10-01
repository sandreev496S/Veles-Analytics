from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    .veles-auth-background {
        position: fixed;
        inset: 0;
        z-index: -1;
        overflow: hidden;
        background:
            radial-gradient(circle at 15% 15%, rgba(37, 99, 235, 0.22), transparent 28%),
            radial-gradient(circle at 85% 20%, rgba(14, 165, 233, 0.18), transparent 30%),
            radial-gradient(circle at 50% 100%, rgba(16, 185, 129, 0.10), transparent 28%),
            linear-gradient(135deg, #020617 0%, #0B1120 45%, #020617 100%);
    }

    .veles-auth-spacer {
        height: 8vh;
    }

    .veles-auth-hero-panel {
        padding: 32px 12px;
    }

    .veles-auth-card-header-only {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 30px 30px 0 0;
        padding: 28px 28px 8px 28px;
        box-shadow: 0 20px 55px rgba(0,0,0,0.30);
        backdrop-filter: blur(18px);
        display: flex;
        gap: 16px;
        align-items: center;
    }

    .veles-auth-card-header-only + div {
        background: rgba(15, 23, 42, 0.78);
        border-left: 1px solid rgba(148, 163, 184, 0.22);
        border-right: 1px solid rgba(148, 163, 184, 0.22);
        padding: 10px 28px 0 28px;
        backdrop-filter: blur(18px);
    }
"""

if css.strip() not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)
    path.write_text(text)

print("Added Streamlit-safe auth layout styles.")
