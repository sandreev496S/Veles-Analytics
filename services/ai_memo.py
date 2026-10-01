import os
from typing import Optional

from dotenv import load_dotenv

try:
    from openai import OpenAI
except ModuleNotFoundError:  # Allows the app to start without the optional AI package.
    OpenAI = None  # type: ignore[assignment]

load_dotenv()


def _get_openai_client():
    """Create the OpenAI client only when an AI memo is requested.

    The Streamlit app must remain usable in demo mode without an API key.
    """
    if OpenAI is None:
        raise RuntimeError(
            "AI memo generation is unavailable because the openai package is not installed."
        )

    api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "AI memo generation is disabled because OPENAI_API_KEY is not configured. "
            "Add it to the project's .env file, then restart Streamlit."
        )

    return OpenAI(api_key=api_key)


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


def generate_investment_memo(company_name, summary_df, forecast_df, sensitivity_df, comps_summary_df):
    client = _get_openai_client()

    prompt = f"""
You are an institutional equity research analyst.

Create a concise investment memo based on this DCF output.

Formatting rules:
- Do not use Markdown italics.
- Do not use asterisks for emphasis.
- Do not use underscores.
- Put spaces between numbers, currency symbols, and words.
- Format dollar values clearly, for example "$137.65B", "$330.13 per share", or "$10.24B in FCF".
- Never write compressed phrases like "$137.65billioninthebasecase".
- Never attach words directly to numbers.
- Use clean numbered section headings.

Company: {company_name}

Valuation Summary:
{summary_df.to_string(index=False)}

Base Case Forecast:
{forecast_df.to_string(index=False)}

Sensitivity Matrix:
{sensitivity_df.to_string()}

Comparable Valuation:
{comps_summary_df.to_string(index=False)}

Structure the memo as:

1. Executive Summary
2. Valuation Conclusion
3. Key Drivers
4. Sensitivity Interpretation
5. Comparable Valuation Interpretation
6. Risks
7. Final Investment View

Use professional investment banking / equity research language.
Do not overstate certainty.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional financial analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return clean_memo_text(response.choices[0].message.content)


def generate_biotech_memo(asset_name, valuation_df, forecast_df):
    client = _get_openai_client()

    prompt = f"""
You are a biotech and neurotechnology valuation analyst.

Create a concise professional valuation memo based on this risk-adjusted NPV model.

Formatting rules:
- Do not use Markdown italics.
- Do not use asterisks for emphasis.
- Do not use underscores.
- Put spaces between numbers, currency symbols, and words.
- Format dollar values clearly, for example "$137.65M", "$330.13 per share", or "$10.24B in revenue".
- Never write compressed phrases like "$137.65millioninthebasecase".
- Never attach words directly to numbers.
- Use clean numbered section headings.

Asset / Company: {asset_name}

rNPV Valuation Summary:
{valuation_df.to_string(index=False)}

Probability-Adjusted Forecast:
{forecast_df.to_string(index=False)}

Structure the memo as:

1. Executive Summary
2. rNPV Valuation Conclusion
3. Key Value Drivers
4. Clinical / Regulatory Risk
5. Commercialization Risk
6. Sensitivity Considerations
7. Final Investment View

Use professional biotech investment language.
Do not overstate certainty.
Emphasize that rNPV depends heavily on probability of approval, timing, pricing, penetration, and discount rate.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional biotech equity research analyst."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )

    return clean_memo_text(response.choices[0].message.content)
