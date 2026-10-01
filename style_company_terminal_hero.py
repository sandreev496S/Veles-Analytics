from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Research Workspace company terminal hero */
    .veles-company-terminal-hero {
        position: relative;
        overflow: hidden;
        border-radius: 30px;
        padding: 34px 38px;
        margin-bottom: 26px;
        background:
            radial-gradient(circle at 12% 0%, rgba(56,189,248,0.22), transparent 32%),
            linear-gradient(135deg, rgba(15,23,42,0.95), rgba(2,6,23,0.80));
        border: 1px solid rgba(148,163,184,0.22);
        box-shadow:
            0 28px 72px rgba(0,0,0,0.34),
            inset 0 0 72px rgba(37,99,235,0.05);
        backdrop-filter: blur(18px);
    }

    .veles-company-terminal-hero::before {
        content: "";
        position: absolute;
        inset: 0;
        opacity: 0.14;
        background-image:
            linear-gradient(rgba(148,163,184,0.18) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148,163,184,0.18) 1px, transparent 1px);
        background-size: 42px 42px;
        mask-image: radial-gradient(circle at top left, black, transparent 72%);
    }

    .veles-company-terminal-kicker {
        position: relative;
        color: #38BDF8;
        font-size: 12px;
        font-weight: 950;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .veles-company-terminal-title {
        position: relative;
        color: #F8FAFC;
        font-size: 44px;
        font-weight: 950;
        letter-spacing: -0.055em;
        margin-bottom: 8px;
    }

    .veles-company-terminal-subtitle {
        position: relative;
        color: #CBD5E1;
        font-size: 15px;
        font-weight: 750;
        margin-bottom: 14px;
    }

    .veles-company-terminal-description {
        position: relative;
        color: #94A3B8;
        font-size: 14px;
        line-height: 1.6;
        max-width: 760px;
    }
"""

if "/* Research Workspace company terminal hero */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Company terminal hero styles added.")
