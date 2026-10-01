from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Sidebar logout action */
    [data-testid="stSidebar"] .stButton:has(button[kind="secondary"]):last-of-type > button,
    [data-testid="stSidebar"] button[kind="secondary"] {
        border-radius: 14px;
    }

    [data-testid="stSidebar"] .stButton > button#sidebar_logout,
    [data-testid="stSidebar"] .stButton:has(button[title="Sign out"]) > button {
        color: #94A3B8;
    }

    [data-testid="stSidebar"] div:has(> button[kind="secondary"]) {
        margin-top: 6px;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        color: #F8FAFC;
    }
"""

if "/* Sidebar logout action */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Sidebar logout styling added.")
