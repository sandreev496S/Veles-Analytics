from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Dashboard Research Terminal */
    .veles-terminal-hero {
        position: relative;
        overflow: hidden;
        border-radius: 30px;
        padding: 34px 36px;
        margin-bottom: 28px;
        background:
            radial-gradient(circle at 10% 0%, rgba(37,99,235,0.24), transparent 34%),
            linear-gradient(135deg, rgba(15,23,42,0.92), rgba(2,6,23,0.78));
        border: 1px solid rgba(148,163,184,0.20);
        box-shadow:
            0 28px 72px rgba(0,0,0,0.32),
            inset 0 0 80px rgba(37,99,235,0.05);
        backdrop-filter: blur(18px);
    }

    .veles-terminal-hero::before {
        content: "";
        position: absolute;
        inset: 0;
        opacity: 0.16;
        background-image:
            linear-gradient(rgba(148,163,184,0.18) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148,163,184,0.18) 1px, transparent 1px);
        background-size: 42px 42px;
        mask-image: radial-gradient(circle at top left, black, transparent 70%);
    }

    .veles-terminal-kicker {
        position: relative;
        color: #38BDF8;
        font-size: 12px;
        font-weight: 950;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .veles-terminal-title {
        position: relative;
        color: #F8FAFC;
        font-size: 38px;
        font-weight: 950;
        letter-spacing: -0.045em;
        margin-bottom: 8px;
    }

    .veles-terminal-subtitle {
        position: relative;
        color: #94A3B8;
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 26px;
    }

    .veles-terminal-metrics {
        position: relative;
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
    }

    .veles-terminal-metric {
        padding: 16px 16px;
        border-radius: 18px;
        background: rgba(2,6,23,0.42);
        border: 1px solid rgba(148,163,184,0.16);
    }

    .veles-terminal-metric span {
        display: block;
        color: #94A3B8;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .veles-terminal-metric strong {
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 950;
    }

    .veles-terminal-section-label {
        color: #CBD5E1;
        font-size: 13px;
        font-weight: 900;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin: 6px 0 14px 2px;
    }

    .veles-command-card {
        min-height: 150px;
        padding: 22px;
        border-radius: 24px;
        background:
            linear-gradient(180deg, rgba(15,23,42,0.84), rgba(15,23,42,0.58));
        border: 1px solid rgba(148,163,184,0.18);
        box-shadow: 0 18px 42px rgba(0,0,0,0.24);
        backdrop-filter: blur(14px);
        transition: all 160ms ease;
    }

    .veles-command-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56,189,248,0.34);
        box-shadow:
            0 24px 56px rgba(0,0,0,0.30),
            0 0 42px rgba(37,99,235,0.12);
    }

    .veles-command-icon {
        color: #38BDF8;
        font-size: 26px;
        font-weight: 950;
        margin-bottom: 18px;
    }

    .veles-command-title {
        color: #F8FAFC;
        font-size: 18px;
        font-weight: 900;
        letter-spacing: -0.025em;
        margin-bottom: 8px;
    }

    .veles-command-subtitle {
        color: #94A3B8;
        font-size: 13px;
        line-height: 1.45;
    }
"""

if "/* Dashboard Research Terminal */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Dashboard terminal styles added.")
