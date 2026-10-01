from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0B1220 0%, #111827 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.14);
    }

    .veles-sidebar-brand {
        padding: 8px 4px 26px 4px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.16);
        margin-bottom: 22px;
    }

    .veles-sidebar-logo {
        color: #F8FAFC;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -0.03em;
        margin-bottom: 8px;
    }

    .veles-sidebar-subtitle {
        color: #94A3B8;
        font-size: 12px;
        line-height: 1.45;
        max-width: 210px;
    }

    .veles-nav-section-label {
        color: #64748B;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 20px 0 8px 4px;
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: transparent;
        color: #CBD5E1;
        border: 1px solid transparent;
        border-radius: 14px;
        justify-content: flex-start;
        font-weight: 700;
        padding: 10px 12px;
        margin-bottom: 2px;
        transition: all 0.15s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(59, 130, 246, 0.10);
        border-color: rgba(59, 130, 246, 0.22);
        color: #F8FAFC;
    }

    .veles-sidebar-user-card {
        margin-top: 34px;
        padding: 16px;
        border-radius: 18px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.18);
        box-shadow: 0 14px 32px rgba(0,0,0,0.22);
    }

    .veles-user-name {
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .veles-user-role {
        color: #94A3B8;
        font-size: 12px;
        line-height: 1.45;
    }
"""

if css.strip() not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)
    path.write_text(text)

print("Navigation styles added.")
