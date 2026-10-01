from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Command cards as real links */
    .veles-command-link {
        display: block;
        text-decoration: none !important;
        color: inherit !important;
    }

    .veles-command-link:hover {
        text-decoration: none !important;
    }

    .veles-command-link .veles-command-card {
        cursor: pointer;
    }

    .veles-command-link:hover .veles-command-card {
        transform: translateY(-4px);
        border-color: rgba(56,189,248,0.48);
        box-shadow:
            0 30px 74px rgba(0,0,0,0.38),
            0 0 58px rgba(37,99,235,0.18);
    }

    .veles-command-link:hover .veles-command-card::before {
        opacity: 1;
    }

    .veles-command-link:hover .veles-command-arrow {
        color: #38BDF8;
        transform: translateX(4px);
    }

    div[data-testid="column"]:has(.veles-command-link) .stButton {
        display: none !important;
    }
"""

if "/* Command cards as real links */" not in text:
    text = text.replace("</style>", css + "\n    </style>", 1)

path.write_text(text)
print("Command card link styles added.")
