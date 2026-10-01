from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    .veles-auth-page {
        position: fixed;
        inset: 0;
        z-index: 0;
        overflow: hidden;
        background:
            radial-gradient(circle at 15% 15%, rgba(37, 99, 235, 0.22), transparent 28%),
            radial-gradient(circle at 85% 20%, rgba(14, 165, 233, 0.18), transparent 30%),
            radial-gradient(circle at 50% 100%, rgba(16, 185, 129, 0.10), transparent 28%),
            linear-gradient(135deg, #020617 0%, #0B1120 45%, #020617 100%);
    }

    .veles-auth-bg-grid {
        position: absolute;
        inset: 0;
        opacity: 0.22;
        background-image:
            linear-gradient(rgba(148,163,184,0.12) 1px, transparent 1px),
            linear-gradient(90deg, rgba(148,163,184,0.12) 1px, transparent 1px);
        background-size: 54px 54px;
        mask-image: radial-gradient(circle at center, black, transparent 72%);
    }

    .veles-auth-page:before,
    .veles-auth-page:after {
        content: "";
        position: absolute;
        width: 42vw;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(56,189,248,0.38), transparent);
        top: 24%;
    }

    .veles-auth-page:before {
        left: 0;
        transform: rotate(18deg);
    }

    .veles-auth-page:after {
        right: 0;
        transform: rotate(-18deg);
    }

    .veles-auth-orb {
        position: absolute;
        width: 420px;
        height: 420px;
        border-radius: 999px;
        filter: blur(80px);
        opacity: 0.22;
        animation: velesFloat 8s ease-in-out infinite alternate;
    }

    .veles-auth-orb-left {
        left: -140px;
        bottom: 10%;
        background: #2563EB;
    }

    .veles-auth-orb-right {
        right: -140px;
        top: 8%;
        background: #06B6D4;
        animation-delay: 1.2s;
    }

    @keyframes velesFloat {
        from { transform: translateY(0px) scale(1); }
        to { transform: translateY(-28px) scale(1.04); }
    }

    .veles-auth-shell {
        position: relative;
        max-width: 1180px;
        margin: 9vh auto 0 auto;
        padding: 0 32px;
        display: grid;
        grid-template-columns: 1.15fr 0.85fr;
        gap: 56px;
        align-items: center;
    }

    .veles-auth-hero {
        padding: 34px 0;
    }

    .veles-auth-kicker {
        color: #38BDF8;
        font-size: 13px;
        font-weight: 950;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 22px;
    }

    .veles-auth-title {
        color: #F8FAFC;
        font-size: clamp(42px, 5vw, 72px);
        line-height: 0.96;
        font-weight: 950;
        letter-spacing: -0.065em;
        max-width: 760px;
        margin-bottom: 24px;
    }

    .veles-auth-subtitle {
        color: #94A3B8;
        font-size: 17px;
        line-height: 1.75;
        max-width: 660px;
        margin-bottom: 34px;
    }

    .veles-auth-feature-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
        max-width: 650px;
    }

    .veles-auth-feature {
        color: #CBD5E1;
        background: rgba(15, 23, 42, 0.62);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 16px;
        padding: 13px 14px;
        font-size: 13px;
        font-weight: 800;
        backdrop-filter: blur(12px);
    }

    .veles-auth-card-wrap {
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 30px;
        padding: 26px;
        box-shadow: 0 28px 70px rgba(0,0,0,0.42);
        backdrop-filter: blur(18px);
    }

    .veles-auth-card-header {
        display: flex;
        align-items: center;
        gap: 16px;
    }

    .veles-auth-logo-mark {
        width: 54px;
        height: 54px;
        display: grid;
        place-items: center;
        border-radius: 18px;
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 950;
        background: linear-gradient(135deg, #2563EB, #06B6D4);
        box-shadow: 0 18px 38px rgba(37, 99, 235, 0.28);
    }

    .veles-auth-card-title {
        color: #F8FAFC;
        font-size: 28px;
        font-weight: 900;
        letter-spacing: -0.04em;
    }

    .veles-auth-card-caption {
        color: #94A3B8;
        font-size: 14px;
        margin-top: 3px;
    }

    .veles-auth-form-card {
        position: relative;
        margin-top: -330px;
        background: rgba(15, 23, 42, 0.78);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 30px;
        padding: 150px 28px 28px 28px;
        box-shadow: 0 28px 70px rgba(0,0,0,0.42);
        backdrop-filter: blur(18px);
    }

    .veles-auth-footnote {
        margin-top: 18px;
        color: #64748B;
        font-size: 12px;
        text-align: center;
        line-height: 1.5;
    }

    .veles-auth-form-card .stButton > button {
        background: linear-gradient(90deg, #2563EB, #06B6D4);
        color: white;
        border: 0;
        border-radius: 14px;
        font-weight: 900;
        height: 48px;
        box-shadow: 0 18px 36px rgba(37,99,235,0.28);
    }

    .veles-auth-form-card .stTextInput input {
        background: rgba(2, 6, 23, 0.62);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 14px;
        color: #F8FAFC;
    }

    .veles-auth-form-card [data-testid="stRadio"] label {
        color: #CBD5E1;
    }

    @media (max-width: 980px) {
        .veles-auth-shell {
            grid-template-columns: 1fr;
            margin-top: 4vh;
            gap: 24px;
        }

        .veles-auth-feature-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        .veles-auth-form-card {
            margin-top: 20px;
            padding-top: 28px;
        }
    }
"""

if css.strip() not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)
    path.write_text(text)

print("Fullscreen auth styles added.")
