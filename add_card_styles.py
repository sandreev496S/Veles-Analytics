from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    .veles-glass-card {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.20);
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 20px;
        box-shadow: 0 18px 42px rgba(0,0,0,0.24);
        backdrop-filter: blur(14px);
    }

    .veles-card-eyebrow {
        color: #38BDF8;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .veles-card-title {
        color: #F8FAFC;
        font-size: 22px;
        font-weight: 850;
        margin-bottom: 8px;
    }

    .veles-card-body {
        color: #CBD5E1;
        font-size: 15px;
        line-height: 1.65;
    }

    .veles-kpi-card {
        background: linear-gradient(180deg, rgba(15,23,42,0.92), rgba(15,23,42,0.70));
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 24px;
        padding: 24px;
        margin-bottom: 18px;
        box-shadow: 0 18px 42px rgba(0,0,0,0.25);
        backdrop-filter: blur(14px);
    }

    .veles-kpi-label {
        color: #94A3B8;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .veles-kpi-value {
        color: #F8FAFC;
        font-size: 34px;
        font-weight: 900;
        margin-top: 10px;
    }

    .veles-kpi-positive {
        color: #10B981;
        font-size: 13px;
        font-weight: 700;
        margin-top: 8px;
    }

    .veles-kpi-negative {
        color: #EF4444;
        font-size: 13px;
        font-weight: 700;
        margin-top: 8px;
    }
"""

if css.strip() not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)
    path.write_text(text)

print("Card styles added.")
