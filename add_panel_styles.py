from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    .veles-panel-header {
        margin-top: 26px;
        margin-bottom: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.18);
    }

    .veles-panel-title {
        color: #F8FAFC;
        font-size: 22px;
        font-weight: 850;
        letter-spacing: -0.02em;
    }

    .veles-panel-subtitle {
        color: #94A3B8;
        font-size: 14px;
        margin-top: 6px;
        line-height: 1.5;
    }
"""

if css.strip() not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)
    path.write_text(text)

print("Panel styles added.")
