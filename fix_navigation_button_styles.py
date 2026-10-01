from pathlib import Path

path = Path("styles.py")
text = path.read_text()

bad_css = '''
    section[data-testid="stSidebar"] .stButton > button {
        height: 0;
        min-height: 0;
        padding: 0;
        margin: 0 0 2px 0;
        opacity: 0;
        border: 0;
    }
'''

text = text.replace(bad_css, "")

css = """
    .veles-nav-current {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #F8FAFC;
        background: rgba(59, 130, 246, 0.14);
        border: 1px solid rgba(59, 130, 246, 0.35);
        border-left: 3px solid #38BDF8;
        border-radius: 14px;
        padding: 10px 12px;
        margin: 4px 0 6px 0;
        font-size: 14px;
        font-weight: 800;
        box-shadow: 0 10px 28px rgba(37, 99, 235, 0.18);
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: transparent;
        color: #CBD5E1;
        border: 1px solid transparent;
        border-radius: 14px;
        justify-content: flex-start;
        font-weight: 700;
        padding: 10px 12px;
        margin-bottom: 4px;
        transition: all 0.15s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(59, 130, 246, 0.10);
        border-color: rgba(59, 130, 246, 0.22);
        color: #F8FAFC;
    }
"""

if ".veles-nav-current" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Navigation button styles fixed.")
