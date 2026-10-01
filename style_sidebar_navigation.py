from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Navigation redesign sprint */
    [data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 20% 0%, rgba(37, 99, 235, 0.18), transparent 34%),
            linear-gradient(180deg, #020617 0%, #07111F 52%, #020617 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.14);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 28px;
    }

    .veles-sidebar-brand {
        padding: 18px 16px 20px 16px;
        margin-bottom: 18px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.14);
    }

    .veles-sidebar-logo {
        color: #F8FAFC;
        font-size: 18px;
        font-weight: 950;
        letter-spacing: 0.08em;
    }

    .veles-sidebar-subtitle {
        color: #94A3B8;
        font-size: 12px;
        line-height: 1.4;
        margin-top: 6px;
    }

    .veles-nav-section-label {
        color: #64748B;
        font-size: 11px;
        font-weight: 850;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin: 20px 10px 8px 10px;
    }

    .veles-nav-current {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 4px 4px;
        padding: 11px 12px;
        border-radius: 14px;
        color: #F8FAFC;
        font-size: 14px;
        font-weight: 850;
        background:
            linear-gradient(90deg, rgba(37, 99, 235, 0.30), rgba(6, 182, 212, 0.12));
        border: 1px solid rgba(96, 165, 250, 0.36);
        box-shadow:
            0 14px 34px rgba(37, 99, 235, 0.18),
            inset 3px 0 0 rgba(56, 189, 248, 0.95);
    }

    .veles-nav-icon {
        color: #67E8F9;
        width: 18px;
        display: inline-flex;
        justify-content: center;
    }

    [data-testid="stSidebar"] .stButton > button {
        justify-content: flex-start;
        background: transparent;
        color: #CBD5E1;
        border: 1px solid transparent;
        border-radius: 14px;
        padding: 10px 12px;
        font-size: 14px;
        font-weight: 700;
        transition:
            background 160ms ease,
            border-color 160ms ease,
            color 160ms ease,
            transform 160ms ease;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(15, 23, 42, 0.72);
        border-color: rgba(148, 163, 184, 0.20);
        color: #F8FAFC;
        transform: translateX(2px);
    }

    [data-testid="stSidebar"] .stButton > button:focus,
    [data-testid="stSidebar"] .stButton > button:active {
        background: rgba(37, 99, 235, 0.16);
        border-color: rgba(96, 165, 250, 0.28);
        color: #F8FAFC;
        box-shadow: none;
    }

    .veles-sidebar-user-card {
        margin: 28px 6px 12px 6px;
        padding: 14px 14px;
        border-radius: 16px;
        background: rgba(15, 23, 42, 0.72);
        border: 1px solid rgba(148, 163, 184, 0.16);
    }

    .veles-user-name {
        color: #F8FAFC;
        font-size: 13px;
        font-weight: 850;
    }

    .veles-user-role {
        color: #64748B;
        font-size: 11px;
        margin-top: 4px;
    }
"""

if "/* Navigation redesign sprint */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Sidebar navigation styling added.")
