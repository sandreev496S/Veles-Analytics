from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* DCF workflow spacing fix */
    .veles-sticky-workflow {
        padding: 0 !important;
        margin: 0 0 22px 0 !important;
        min-height: auto !important;
        height: auto !important;
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
    }
"""

if "/* DCF workflow spacing fix */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("DCF sticky workflow spacing fixed.")
