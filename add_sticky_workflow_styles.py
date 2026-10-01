from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    .veles-sticky-workflow {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(15, 23, 42, 0.92);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 22px;
        padding: 16px 18px;
        margin-bottom: 22px;
        box-shadow: 0 18px 42px rgba(0,0,0,0.28);
        backdrop-filter: blur(16px);
    }
"""

if css.strip() not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)
    path.write_text(text)

print("Sticky workflow styles added.")
