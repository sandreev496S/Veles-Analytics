from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Final login polish */
    .veles-auth-title {
        max-width: 720px;
    }

    .veles-auth-subtitle {
        max-width: 620px;
        margin-bottom: 22px;
    }

    .veles-auth-feature-grid {
        margin-top: 0;
    }

    #MainMenu {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        display: none;
    }

    [data-testid="stToolbar"] {
        display: none;
    }

    [data-testid="stDecoration"] {
        display: none;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
    }
"""

if "/* Final login polish */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Final login polish added.")
