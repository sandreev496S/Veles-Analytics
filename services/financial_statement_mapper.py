import re
import warnings
import pandas as pd


IGNORE_SHEET_TERMS = [
    "table_of_contents",
    "table of contents",
    "contents",
    "cover",
    "document",
    "metadata",
]


SHEET_SCORE_TERMS = {
    "revenue": 5,
    "net sales": 5,
    "net income": 5,
    "assets": 5,
    "liabilities": 5,
    "cash": 5,
    "cash and cash equivalents": 7,
    "total assets": 7,
    "total liabilities": 7,
    "shareholders equity": 5,
    "stockholders equity": 5,
    "statement of operations": 8,
    "income statement": 8,
    "balance sheet": 8,
    "cash flow": 6,
}


def normalize_text(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def is_ignored_sheet(sheet_name):
    normalized = normalize_text(sheet_name)
    return any(term.replace("_", " ") in normalized for term in IGNORE_SHEET_TERMS)


def score_dataframe(df):
    if df is None or df.empty:
        return 0

    sample = df.head(80).astype(str).fillna("")
    text_blob = normalize_text(" ".join(sample.values.flatten().tolist()))

    score = 0
    for term, weight in SHEET_SCORE_TERMS.items():
        if normalize_text(term) in text_blob:
            score += weight

    return score


def find_best_financial_sheets(excel_file, min_score=5):
    scored = []

    for sheet_name in excel_file.sheet_names:
        if is_ignored_sheet(sheet_name):
            continue

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                df = pd.read_excel(excel_file, sheet_name=sheet_name, header=None)
        except Exception:
            continue

        score = score_dataframe(df)

        if score >= min_score:
            scored.append(
                {
                    "sheet_name": sheet_name,
                    "score": score,
                    "dataframe": df,
                }
            )

    return sorted(scored, key=lambda item: item["score"], reverse=True)


def find_best_financial_sheet(excel_file, min_score=5):
    sheets = find_best_financial_sheets(excel_file, min_score=min_score)
    return sheets[0] if sheets else None
