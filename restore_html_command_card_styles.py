from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Restored premium HTML command cards */
    .veles-command-card {
        position: relative;
        min-height: 190px;
        padding: 26px 28px;
        border-radius: 28px;
        background:
            radial-gradient(circle at 10% 12%, rgba(56,189,248,0.18), transparent 30%),
            linear-gradient(180deg, rgba(15,23,42,0.96), rgba(2,6,23,0.82));
        border: 1px solid rgba(148,163,184,0.22);
        box-shadow:
            0 22px 56px rgba(0,0,0,0.32),
            inset 0 0 42px rgba(37,99,235,0.05);
        transition: all 180ms ease;
        overflow: hidden;
    }

    .veles-command-card::before {
        content: "";
        position: absolute;
        inset: 0;
        opacity: 0;
        background:
            linear-gradient(135deg, rgba(56,189,248,0.12), transparent 38%);
        transition: opacity 180ms ease;
    }

    .veles-command-topline {
        position: relative;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 42px;
        z-index: 1;
    }

    .veles-command-icon {
        width: 44px;
        height: 44px;
        display: grid;
        place-items: center;
        border-radius: 15px;
        color: #38BDF8;
        background: rgba(56,189,248,0.09);
        border: 1px solid rgba(56,189,248,0.20);
        font-size: 20px;
        font-weight: 950;
        box-shadow: inset 0 0 18px rgba(56,189,248,0.08);
    }

    .veles-command-arrow {
        color: #64748B;
        font-size: 20px;
        font-weight: 950;
        transition: all 180ms ease;
    }

    .veles-command-title {
        position: relative;
        z-index: 1;
        color: #F8FAFC;
        font-size: 21px;
        font-weight: 950;
        letter-spacing: -0.04em;
        margin-bottom: 9px;
    }

    .veles-command-subtitle {
        position: relative;
        z-index: 1;
        color: #94A3B8;
        font-size: 13px;
        line-height: 1.5;
        max-width: 260px;
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-card {
        transform: translateY(-4px);
        border-color: rgba(56,189,248,0.48);
        box-shadow:
            0 30px 74px rgba(0,0,0,0.38),
            0 0 58px rgba(37,99,235,0.18);
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-card::before {
        opacity: 1;
    }

    div[data-testid="column"]:has(.veles-command-card):hover .veles-command-arrow {
        color: #38BDF8;
        transform: translateX(4px);
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton {
        margin-top: -190px;
        height: 190px;
        position: relative;
        z-index: 10;
    }

    div[data-testid="column"]:has(.veles-command-card) .stButton > button {
        height: 190px !important;
        min-height: 190px !important;
        opacity: 0 !important;
        border: 0 !important;
        background: transparent !important;
        cursor: pointer !important;
    }
"""

if "/* Restored premium HTML command cards */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Restored premium command card styles.")
