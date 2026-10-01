from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Remove Streamlit chrome */
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
"""

if "/* Remove Streamlit chrome */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Streamlit chrome hidden.")
