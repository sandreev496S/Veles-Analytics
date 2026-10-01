from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    .veles-nav-active-label {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #F8FAFC;
        background: rgba(59, 130, 246, 0.14);
        border: 1px solid rgba(59, 130, 246, 0.35);
        border-left: 3px solid #38BDF8;
        border-radius: 14px;
        padding: 10px 12px;
        margin: 4px 0 2px 0;
        font-size: 14px;
        font-weight: 800;
        box-shadow: 0 10px 28px rgba(37, 99, 235, 0.18);
    }

    .veles-nav-inactive-label {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #CBD5E1;
        padding: 10px 12px;
        margin: 4px 0 2px 0;
        font-size: 14px;
        font-weight: 700;
    }

    .veles-nav-icon {
        width: 18px;
        display: inline-block;
        color: #38BDF8;
    }

    section[data-testid="stSidebar"] .stButton > button {
        height: 0;
        min-height: 0;
        padding: 0;
        margin: 0 0 2px 0;
        opacity: 0;
        border: 0;
    }
"""

if css.strip() not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)
    path.write_text(text)

print("Navigation active styles added.")
