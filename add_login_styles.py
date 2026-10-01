from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    .veles-login-shell {
        max-width: 980px;
        margin: 7vh auto 28px auto;
        text-align: center;
    }

    .veles-login-brand {
        color: #38BDF8;
        font-size: 14px;
        font-weight: 900;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        margin-bottom: 14px;
    }

    .veles-login-title {
        color: #F8FAFC;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: -0.04em;
        margin-bottom: 10px;
    }

    .veles-login-subtitle {
        color: #94A3B8;
        font-size: 16px;
        line-height: 1.6;
        max-width: 680px;
        margin: 0 auto;
    }

    .veles-login-card {
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 26px;
        padding: 28px;
        box-shadow: 0 22px 55px rgba(0,0,0,0.30);
        backdrop-filter: blur(16px);
    }

    .veles-login-info-card {
        background: linear-gradient(180deg, rgba(15,23,42,0.92), rgba(30,41,59,0.74));
        border: 1px solid rgba(56, 189, 248, 0.22);
        border-radius: 26px;
        padding: 30px;
        box-shadow: 0 22px 55px rgba(0,0,0,0.30);
        color: #CBD5E1;
        min-height: 300px;
    }

    .veles-login-info-title {
        color: #F8FAFC;
        font-size: 22px;
        font-weight: 850;
        margin-bottom: 18px;
    }

    .veles-login-info-card li {
        margin-bottom: 12px;
        line-height: 1.5;
    }
"""

if css.strip() not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)
    path.write_text(text)

print("Login styles added.")
