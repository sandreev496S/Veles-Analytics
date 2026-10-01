import re
import warnings
import pandas as pd

from services.financial_statement_mapper import find_best_financial_sheets, score_dataframe


FIELD_RULES = {
    "starting_revenue": {
        "label": "Starting Revenue",
        "include": ["net sales", "total net sales", "revenue", "total revenue"],
        "exclude": ["deferred", "unearned", "segment", "geographic", "contract"],
    },
    "cash": {
        "label": "Cash & Equivalents",
        "include": ["cash and cash equivalents", "cash cash equivalents"],
        "exclude": ["restricted", "supplemental", "cash flows"],
    },
    "shares": {
        "label": "Diluted Shares",
        "include": [
            "shares used in computing diluted",
            "diluted shares",
            "weighted average diluted shares",
        ],
        "exclude": ["basic", "repurchased", "authorized"],
    },
}


DEBT_COMPONENTS = {
    "commercial_paper": ["commercial paper"],
    "current_debt": ["current portion of term debt", "current maturities of long term debt"],
    "term_debt": ["term debt", "long term debt", "long term notes", "notes payable"],
    "total_debt": ["total debt", "total borrowings"],
}


def _norm(x):
    return re.sub(r"[^a-z0-9]+", " ", str(x).lower()).strip()


def _title_company_name(value):
    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)
    return value.title().replace("Inc.", "Inc.").replace("Llc", "LLC")


def _num(x):
    if pd.isna(x):
        return None

    s = str(x).replace(",", "").replace("$", "").strip()

    if s.startswith("(") and s.endswith(")"):
        s = "-" + s[1:-1]

    s = re.sub(r"[^\d.\-]", "", s)

    if s in ["", "-", ".", "-."]:
        return None

    try:
        return float(s)
    except Exception:
        return None


def _financial_numbers(row_values, min_abs=0):
    nums = []

    for raw in row_values:
        n = _num(raw)

        if n is None:
            continue

        if 1900 <= n <= 2100:
            continue

        if abs(n) < min_abs:
            continue

        nums.append(n)

    return nums


def _latest_financial_value(row_values, min_abs=0):
    nums = _financial_numbers(row_values, min_abs=min_abs)
    return nums[0] if nums else None


def _match_field(label, field):
    rule = FIELD_RULES[field]
    return (
        any(term in label for term in rule["include"])
        and not any(term in label for term in rule["exclude"])
    )


def _debt_component_kind(label):
    for component, terms in DEBT_COMPONENTS.items():
        if any(term in label for term in terms):
            return component
    return None


def _detect_company_name(frames):
    company_suffixes = [
        " INC",
        " INC.",
        " CORPORATION",
        " CORP",
        " CORP.",
        " PLC",
        " LTD",
        " LTD.",
        " LIMITED",
    ]

    bad_terms = [
        "form type",
        "period end",
        "date filed",
        "table of contents",
        "created by",
        "consolidated",
        "statement",
        "income",
        "balance",
        "cash flow",
        "document",
        "table",
    ]

    candidates = []

    for sheet_name, df in frames:
        sample = df.head(120).astype(str).fillna("")

        for row_index, row in sample.iterrows():
            values = [str(v).strip() for v in row.values if str(v).strip() and str(v).strip().lower() != "nan"]

            for idx, raw in enumerate(values):
                upper = raw.upper().strip()
                normalized = _norm(raw)

                if not raw or any(term in normalized for term in bad_terms):
                    continue

                # Reject SEC/random file hashes.
                if re.fullmatch(r"[A-Fa-f0-9]{16,}", raw.replace("-", "")):
                    continue

                # Prefer explicit company-like all-caps issuer names.
                score = 0

                if any(suffix in f" {upper}" for suffix in company_suffixes):
                    score += 60

                if upper == raw and len(raw) >= 4:
                    score += 10

                if sheet_name and "cover" in _norm(sheet_name):
                    score += 20

                if "APPLE" in upper or "MICROSOFT" in upper or "NVIDIA" in upper or "META" in upper:
                    score += 20

                # Very long hash-like strings are bad company names.
                if len(raw) > 60:
                    score -= 30

                if score > 0:
                    candidates.append((score, raw))

    if not candidates:
        return None

    best = sorted(candidates, key=lambda item: item[0], reverse=True)[0][1]
    return _title_company_name(best)


def parse_financial_statement(file):
    file_name = file.name.lower()
    frames = []
    sheet_scores = []

    if file_name.endswith(".csv"):
        csv_df = pd.read_csv(file, header=None)
        frames.append(("CSV", csv_df))
        sheet_scores.append({"Sheet": "CSV", "Score": score_dataframe(csv_df), "Selected": True})
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            excel = pd.ExcelFile(file)

        best_sheets = find_best_financial_sheets(excel)

        if best_sheets:
            selected_names = {item["sheet_name"] for item in best_sheets}

            for item in best_sheets:
                frames.append((item["sheet_name"], item["dataframe"]))

            for sheet in excel.sheet_names:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    try:
                        score_df = pd.read_excel(excel, sheet_name=sheet, header=None)
                        sheet_scores.append({
                            "Sheet": sheet,
                            "Score": score_dataframe(score_df),
                            "Selected": sheet in selected_names,
                        })
                    except Exception:
                        sheet_scores.append({"Sheet": sheet, "Score": 0, "Selected": False})
        else:
            for sheet in excel.sheet_names:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    sheet_df = pd.read_excel(excel, sheet_name=sheet, header=None)
                    frames.append((sheet, sheet_df))
                    sheet_scores.append({
                        "Sheet": sheet,
                        "Score": score_dataframe(sheet_df),
                        "Selected": True,
                    })

    parsed = {}
    detected_rows = []

    company_name = _detect_company_name(frames)
    if company_name:
        parsed["company_name"] = company_name

    candidates = []
    debt_components = {}

    for sheet_name, df in frames:
        df = df.dropna(how="all").dropna(axis=1, how="all")

        if df.empty:
            continue

        for _, row in df.iterrows():
            row_values = list(row.values)
            label = _norm(" ".join(str(v) for v in row_values[:4] if pd.notna(v)))

            alpha_chars = re.sub(r"[^a-z]+", "", label)
            if len(alpha_chars) < 4:
                continue

            for field in FIELD_RULES:
                if _match_field(label, field):
                    min_abs = 1000 if field == "starting_revenue" else 0
                    value = _latest_financial_value(row_values, min_abs=min_abs)

                    if value is not None:
                        candidates.append({
                            "field": field,
                            "Detected Field": FIELD_RULES[field]["label"],
                            "Detected Value": value,
                            "Confidence": "High",
                            "Source Sheet": sheet_name,
                            "Source Label": label[:180],
                        })

            component_kind = _debt_component_kind(label)
            if component_kind:
                value = _latest_financial_value(row_values)

                if value is not None:
                    debt_components.setdefault(component_kind, {
                        "Detected Field": "Total Debt",
                        "Detected Value": abs(value),
                        "Confidence": "Medium",
                        "Source Sheet": sheet_name,
                        "Source Label": label[:180],
                    })

    for field in FIELD_RULES:
        field_candidates = [c for c in candidates if c["field"] == field]

        if not field_candidates:
            continue

        best = field_candidates[0]
        parsed[field] = best["Detected Value"]

        detected_rows.append({
            "Detected Field": best["Detected Field"],
            "Detected Value": best["Detected Value"],
            "Confidence": best["Confidence"],
            "Source Sheet": best["Source Sheet"],
            "Source Label": best["Source Label"],
        })

    if "total_debt" in debt_components:
        debt_value = debt_components["total_debt"]["Detected Value"]
        debt_source = debt_components["total_debt"]
    elif debt_components:
        debt_value = sum(item["Detected Value"] for item in debt_components.values())
        debt_source = {
            "Detected Field": "Total Debt",
            "Detected Value": debt_value,
            "Confidence": "Medium",
            "Source Sheet": " + ".join(sorted({item["Source Sheet"] for item in debt_components.values()})),
            "Source Label": "rolled up from: " + ", ".join(sorted(debt_components.keys())),
        }
    else:
        debt_value = None
        debt_source = None

    if debt_value is not None:
        parsed["debt"] = debt_value
        detected_rows.append(debt_source)

    if "shares" in parsed and parsed["shares"] > 1_000_000:
        parsed["shares"] = parsed["shares"] / 1000

        for row in detected_rows:
            if row.get("Detected Field") == "Diluted Shares":
                row["Detected Value"] = parsed["shares"]
                row["Source Label"] = f"{row.get('Source Label', '')} | normalized to millions"

    detected_df = pd.DataFrame(detected_rows)

    if sheet_scores:
        score_df = pd.DataFrame(sheet_scores).sort_values(
            ["Selected", "Score"],
            ascending=[False, False],
        )
        detected_df.attrs["sheet_scores"] = score_df

    return parsed, detected_df
