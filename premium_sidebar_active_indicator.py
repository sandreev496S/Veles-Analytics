from pathlib import Path

path = Path("styles.py")
text = path.read_text()

css = """
    /* Premium sidebar active indicator */
    .veles-nav-current {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(
                90deg,
                rgba(37,99,235,0.24),
                rgba(6,182,212,0.10)
            );
        border: 1px solid rgba(96,165,250,0.34);
        box-shadow:
            0 14px 36px rgba(37,99,235,0.20),
            inset 0 0 22px rgba(56,189,248,0.05);
    }

    .veles-nav-current::before {
        content: "";
        position: absolute;
        left: 0;
        top: 10px;
        bottom: 10px;
        width: 4px;
        border-radius: 999px;
        background: linear-gradient(
            180deg,
            #38BDF8,
            #2563EB
        );
        box-shadow:
            0 0 16px rgba(56,189,248,0.65);
    }

    .veles-nav-current .veles-nav-icon {
        color: #67E8F9;
    }
"""

if "/* Premium sidebar active indicator */" not in text:
    text = text.replace(
        "</style>",
        css + "\n    </style>",
        1,
    )

path.write_text(text)
print("Premium active indicator added.")
