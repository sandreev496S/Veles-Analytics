from pathlib import Path

path = Path("services/ai_memo.py")
text = path.read_text()

if "def clean_memo_text" not in text:
    text = text.replace(
        "client = OpenAI(api_key=os.getenv(\"OPENAI_API_KEY\"))\n\n",
        '''client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def clean_memo_text(text):
    if not text:
        return ""

    replacements = {
        "$ ": "$",
        " ,": ",",
        " .": ".",
        " %": "%",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("*", "")
    text = text.replace("_", "")

    return text.strip()


''',
        1,
    )

text = text.replace(
    "Create a concise investment memo based on this DCF output.",
    '''Create a concise investment memo based on this DCF output.

Formatting rules:
- Do not use Markdown italics.
- Do not use asterisks for emphasis.
- Do not use underscores.
- Put spaces between numbers, currency symbols, and words.
- Format dollar values clearly, for example "$137.65B", "$330.13 per share", or "$10.24B in FCF".
- Never write compressed phrases like "$137.65billioninthebasecase".
- Never attach words directly to numbers.
- Use clean numbered section headings.''',
    1,
)

text = text.replace(
    "Create a concise professional valuation memo based on this risk-adjusted NPV model.",
    '''Create a concise professional valuation memo based on this risk-adjusted NPV model.

Formatting rules:
- Do not use Markdown italics.
- Do not use asterisks for emphasis.
- Do not use underscores.
- Put spaces between numbers, currency symbols, and words.
- Format dollar values clearly, for example "$137.65M", "$330.13 per share", or "$10.24B in revenue".
- Never write compressed phrases like "$137.65millioninthebasecase".
- Never attach words directly to numbers.
- Use clean numbered section headings.''',
    1,
)

text = text.replace(
    "    return response.choices[0].message.content",
    "    return clean_memo_text(response.choices[0].message.content)",
)

path.write_text(text)
print("AI memo formatting rules and sanitizer added.")
