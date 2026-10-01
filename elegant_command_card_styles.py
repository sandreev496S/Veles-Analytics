from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Elegant command center cards */
    .veles-command-card {
        min-height: 172px;
        padding: 24px;
        border-radius: 26px;
        background:
            radial-gradient(circle at 12% 10%, rgba(56,189,248,0.18), transparent 32%),
            linear-gradient(180deg, rgba(15,23,42,0.92), rgba(2,6,23,0.78));
        border: 1px solid rgba(148,163,184,0.20);
        box-shadow:
            0 20px 48px rgba(0,0,0,0.28),
            inset 0 0 42px rgba(37,99,235,0.04);
        transition: all 180ms ease;
    }

    .veles-command-topline {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
    }

    .veles-command-icon {
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        border-radius: 14px;
        color: #38BDF8;
        background: rgba(56,189,248,0.08);
        border: 1px solid rgba(56,189,248,0.18);
        font-size: 20px;
        font-weight: 950;
    }

    .veles-command-arrow {
        color: #64748B;
        font-size: 18px;
        font-weight: 900;
        transition: all 160ms ease;
    }

    .veles-command-title {
        color: #F8FAFC;
        font-size: 19px;
        font-weight: 950;
        letter-spacing: -0.035em;
        margin-bottom: 8px;
    }

    .veles-command-subtitle {
        color: #94A3B8;
        font-size: 13px;
        line-height: 1.45;
        max-width: 190px;
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-card {
        transform: translateY(-3px);
        border-color: rgba(56,189,248,0.42);
        box-shadow:
            0 28px 68px rgba(0,0,0,0.36),
            0 0 52px rgba(37,99,235,0.14);
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-arrow {
        color: #38BDF8;
        transform: translateX(3px);
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button {
        margin-top: -52px;
        height: 44px;
        border-radius: 0 0 22px 22px;
        border: 1px solid rgba(56,189,248,0.16);
        border-top: 0;
        background: rgba(2,6,23,0.34);
        color: #38BDF8;
        font-size: 11px;
        font-weight: 950;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        transition: all 160ms ease;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button:hover {
        background: rgba(37,99,235,0.18);
        color: #F8FAFC;
        border-color: rgba(56,189,248,0.34);
    }
"""

if "/* Elegant command center cards */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Elegant command card styles added.")
