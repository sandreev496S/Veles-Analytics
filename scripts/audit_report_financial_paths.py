from __future__ import annotations

import ast
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]

TARGET_DIRECTORIES = (
    PROJECT_ROOT / "services" / "reports",
    PROJECT_ROOT / "services" / "charts",
    PROJECT_ROOT / "services" / "pdf",
)

TARGET_FILES = (
    PROJECT_ROOT / "services" / "pdf_report.py",
    PROJECT_ROOT / "services" / "pdf_report_exporter.py",
    PROJECT_ROOT / "services" / "equity_report_engine.py",
)

OUTPUT_PATH = PROJECT_ROOT / "report_financial_audit.md"


FINANCIAL_TERMS = {
    "share_price",
    "market_cap",
    "enterprise_value",
    "provider_enterprise_value",
    "cash",
    "cash_and_cash_equivalents",
    "restricted_cash",
    "debt",
    "financial_debt",
    "total_debt",
    "equity",
    "revenue",
    "rd_expense",
    "r_and_d",
    "research_and_development",
    "operating_income",
    "operating_loss",
    "net_income",
    "free_cash_flow",
    "operating_cash_flow",
    "capital_expenditures",
    "cash_burn",
    "burn",
    "runway",
    "growth",
    "margin",
    "multiple",
    "price_to_book",
    "price_to_sales",
    "ev_to_revenue",
    "valuation",
    "profitability",
    "liquidity",
}


PREPARED_REPORT_TABLE_FIELDS = {
    "income_statement",
    "balance_sheet",
    "cash_flow",
    "market_snapshot",
    "valuation_multiples",
    "financial_table",
}


RAW_DATA_PATH_TERMS = {
    "raw",
    "financials",
    "market",
    "sec",
    "income_statement",
    "balance_sheet",
    "cash_flow",
    "metrics",
    "market_snapshot",
    "valuation_multiples",
}


FORMAT_FUNCTION_NAMES = {
    "format",
    "format_money",
    "_format_money",
    "format_currency",
    "format_percent",
    "_format_percent",
    "_fmt_money",
    "_fmt_num",
}


CALCULATION_FUNCTION_NAMES = {
    "sum",
    "mean",
    "median",
    "abs",
    "min",
    "max",
    "round",
}


FORMATTED_VALUE_PARSERS = {
    "_parse_money",
    "parse_money",
    "parse_currency",
}


LEGACY_TABLE_EXTRACTORS = {
    "_get_statement_value",
    "_table_to_dict",
    "_latest_value",
    "_statement_values",
}


SEMANTIC_STATE_NAMES = {
    "state",
    "status",
    "classification",
    "direction",
    "risk",
    "risk_level",
    "balance_sheet_state",
    "balance_sheet_risk",
    "cash_flow_state",
    "profitability_state",
    "growth_state",
    "liquidity_state",
    "applicability",
    "validation_status",
}


SEMANTIC_STATE_VALUES = {
    "positive",
    "negative",
    "neutral",
    "stable",
    "growing",
    "declining",
    "accelerating",
    "decelerating",
    "profitable",
    "loss_making",
    "cash_generative",
    "cash_burning",
    "net_cash",
    "net_debt",
    "strong",
    "adequate",
    "weak",
    "elevated",
    "high",
    "moderate",
    "low",
    "valid",
    "invalid",
    "resolved",
    "unresolved",
    "applicable",
    "inapplicable",
    "unknown",
}


DISPLAY_SCALE_CONSTANTS = {
    100,
    1_000,
    1_000_000,
    1_000_000_000,
    1_000_000_000_000,
}


LAYOUT_PATH_SUFFIXES = {
    "services/pdf/footer.py",
}


LAYOUT_FUNCTION_TERMS = {
    "page",
    "footer",
    "header",
    "margin",
    "width",
    "height",
    "coordinate",
    "position",
    "layout",
    "spacing",
    "column",
    "row",
    "draw",
    "canvas",
}


DISPLAY_FUNCTION_TERMS = {
    "chart",
    "plot",
    "axis",
    "tick",
    "label",
    "display",
    "render",
    "scale",
    "normalize",
}


@dataclass(frozen=True)
class AuditFinding:
    file: str
    line: int
    function: str
    category: str
    symbol: str
    code: str
    disposition: str
    reason: str
    recommendation: str


def iter_python_files() -> Iterable[Path]:
    found: set[Path] = set()

    for directory in TARGET_DIRECTORIES:
        if not directory.exists():
            continue

        for path in directory.rglob("*.py"):
            if ".bak" in path.name:
                continue

            found.add(path)

    for path in TARGET_FILES:
        if path.exists():
            found.add(path)

    yield from sorted(found)


def source_segment(
    source: str,
    node: ast.AST,
) -> str:
    segment = ast.get_source_segment(source, node)

    if segment:
        return " ".join(segment.strip().split())

    return node.__class__.__name__


def dotted_name(node: ast.AST) -> str | None:
    parts: list[str] = []
    current = node

    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value

    if isinstance(current, ast.Name):
        parts.append(current.id)
        return ".".join(reversed(parts))

    return None


def normalized_identifier(value: str) -> str:
    return re.sub(
        r"[^a-z0-9]+",
        "_",
        value.lower(),
    ).strip("_")


def contains_financial_term(value: str) -> bool:
    normalized = normalized_identifier(value)

    return any(
        term in normalized
        for term in FINANCIAL_TERMS
    )


def constant_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value

    return None


def constant_number(node: ast.AST) -> float | int | None:
    if (
        isinstance(node, ast.Constant)
        and isinstance(node.value, (int, float))
        and not isinstance(node.value, bool)
    ):
        return node.value

    return None


def subscript_path(node: ast.Subscript) -> list[str]:
    parts: list[str] = []
    current: ast.AST = node

    while isinstance(current, ast.Subscript):
        key = constant_string(current.slice)

        if key is not None:
            parts.append(key)
        else:
            parts.append("?")

        current = current.value

    if isinstance(current, ast.Name):
        parts.append(current.id)
    else:
        name = dotted_name(current)
        if name:
            parts.append(name)

    return list(reversed(parts))


def is_raw_financial_path(parts: list[str]) -> bool:
    normalized = {
        normalized_identifier(part)
        for part in parts
    }

    return bool(
        normalized & RAW_DATA_PATH_TERMS
    ) and any(
        contains_financial_term(part)
        for part in parts
    )


def is_prepared_report_path(parts: list[str]) -> bool:
    if len(parts) < 2:
        return False

    root = normalized_identifier(parts[0])
    leaf = normalized_identifier(parts[-1])

    return (
        root in {"report", "report_document", "render_model"}
        and leaf in PREPARED_REPORT_TABLE_FIELDS
    )


def is_render_content_comparison(node: ast.Compare) -> bool:
    expression = normalized_identifier(ast.unparse(node))
    content_terms = {
        "heading",
        "section",
        "title",
        "include_valuation",
        "include_dcf",
        "include_scenarios",
        "include_sensitivity",
    }

    return any(term in expression for term in content_terms)


def is_status_comparison(node: ast.Compare) -> bool:
    operands = [node.left, *node.comparators]

    references_status = any(
        semantic_state_reference(operand)
        for operand in operands
    )
    compares_string = any(
        constant_string(operand) is not None
        for operand in operands
    )

    return references_status and compares_string


def semantic_state_reference(node: ast.AST) -> bool:
    if isinstance(node, ast.Name):
        return normalized_identifier(node.id) in SEMANTIC_STATE_NAMES

    if isinstance(node, ast.Attribute):
        return normalized_identifier(node.attr) in SEMANTIC_STATE_NAMES

    if isinstance(node, ast.Subscript):
        parts = subscript_path(node)
        return any(
            normalized_identifier(part) in SEMANTIC_STATE_NAMES
            for part in parts
        )

    if isinstance(node, ast.Call):
        function_name = dotted_name(node.func)

        if (
            function_name
            and function_name.endswith(".get")
            and node.args
        ):
            key = constant_string(node.args[0])
            return (
                key is not None
                and normalized_identifier(key) in SEMANTIC_STATE_NAMES
            )

    return False


def semantic_state_literal(node: ast.AST) -> bool:
    value = constant_string(node)

    if value is None:
        return False

    return normalized_identifier(value) in SEMANTIC_STATE_VALUES


def is_semantic_state_comparison(node: ast.Compare) -> bool:
    operands = [node.left, *node.comparators]

    has_state_reference = any(
        semantic_state_reference(operand)
        for operand in operands
    )
    has_state_literal = any(
        semantic_state_literal(operand)
        for operand in operands
    )

    return has_state_reference and has_state_literal


def is_display_scale_operation(node: ast.BinOp) -> bool:
    if not isinstance(node.op, (ast.Div, ast.Mult)):
        return False

    left_number = constant_number(node.left)
    right_number = constant_number(node.right)

    numeric_values = {
        value
        for value in (left_number, right_number)
        if value is not None
    }

    return bool(
        numeric_values & DISPLAY_SCALE_CONSTANTS
    )


def is_none_literal(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Constant)
        and node.value is None
    )


def is_availability_comparison(node: ast.Compare) -> bool:
    operands = [node.left, *node.comparators]

    return any(
        is_none_literal(operand)
        for operand in operands
    ) and any(
        contains_financial_term(
            ast.unparse(operand)
        )
        for operand in operands
        if not is_none_literal(operand)
    )


def is_path_join_operation(node: ast.BinOp) -> bool:
    if not isinstance(node.op, ast.Div):
        return False

    right = constant_string(node.right)

    if right is None:
        return False

    left_text = normalized_identifier(
        ast.unparse(node.left)
    )

    return (
        "path" in left_text
        or "dir" in left_text
        or "output" in left_text
    )


def is_type_union_operation(node: ast.BinOp) -> bool:
    if not isinstance(node.op, ast.BitOr):
        return False

    return isinstance(
        node.parent,
        (ast.AnnAssign, ast.arg),
    )


def attach_parents(tree: ast.AST) -> None:
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            child.parent = parent


def is_assessment_policy_path(relative_path: str) -> bool:
    return relative_path in {
        "services/reports/analyst_assessment.py",
        "services/reports/reconciliation.py",
    }


class ReportFinancialAuditVisitor(ast.NodeVisitor):
    def __init__(
        self,
        *,
        path: Path,
        source: str,
    ) -> None:
        self.path = path
        self.source = source
        self.findings: list[AuditFinding] = []
        self.function_stack: list[str] = []

    @property
    def relative_path(self) -> str:
        return str(self.path.relative_to(PROJECT_ROOT))

    @property
    def current_function(self) -> str:
        if not self.function_stack:
            return "<module>"

        return ".".join(self.function_stack)

    def add(
        self,
        node: ast.AST,
        *,
        category: str,
        symbol: str,
        disposition: str,
        reason: str,
        recommendation: str,
    ) -> None:
        self.findings.append(
            AuditFinding(
                file=self.relative_path,
                line=getattr(node, "lineno", 0),
                function=self.current_function,
                category=category,
                symbol=symbol,
                code=source_segment(self.source, node),
                disposition=disposition,
                reason=reason,
                recommendation=recommendation,
            )
        )

    def visit_FunctionDef(
        self,
        node: ast.FunctionDef,
    ) -> None:
        self.function_stack.append(node.name)
        self.generic_visit(node)
        self.function_stack.pop()

    def visit_AsyncFunctionDef(
        self,
        node: ast.AsyncFunctionDef,
    ) -> None:
        self.function_stack.append(node.name)
        self.generic_visit(node)
        self.function_stack.pop()

    def is_layout_context(self) -> bool:
        if self.relative_path in LAYOUT_PATH_SUFFIXES:
            return True

        function_name = normalized_identifier(
            self.current_function
        )

        return any(
            term in function_name
            for term in LAYOUT_FUNCTION_TERMS
        ) and (
            "/pdf/" in f"/{self.relative_path}"
            or self.relative_path.startswith("services/pdf")
        )

    def is_chart_context(self) -> bool:
        if "/charts/" in f"/{self.relative_path}":
            return True

        function_name = normalized_identifier(
            self.current_function
        )

        return any(
            term in function_name
            for term in DISPLAY_FUNCTION_TERMS
        )

    def visit_Subscript(
        self,
        node: ast.Subscript,
    ) -> None:
        parts = subscript_path(node)

        if (
            is_raw_financial_path(parts)
            and not is_prepared_report_path(parts)
        ):
            self.add(
                node,
                category="DIRECT_DATA_ACCESS",
                symbol=" -> ".join(parts),
                disposition="MUST_MIGRATE",
                reason=(
                    "The report pipeline is navigating a raw or normalized "
                    "financial-data structure directly."
                ),
                recommendation=(
                    "Replace this access with ReportFinancialData, "
                    "ValidatedMetric, ValidatedSeries, or a prepared "
                    "render-model field."
                ),
            )

        self.generic_visit(node)

    def visit_Call(
        self,
        node: ast.Call,
    ) -> None:
        function_name = dotted_name(node.func)

        if function_name is None and isinstance(
            node.func,
            ast.Name,
        ):
            function_name = node.func.id

        if function_name:
            short_name = function_name.split(".")[-1]

            if short_name in FORMAT_FUNCTION_NAMES:
                self.add(
                    node,
                    category="FORMATTING",
                    symbol=function_name,
                    disposition="ALLOWED_FORMATTING",
                    reason=(
                        "This call converts an already-derived value into "
                        "presentation text."
                    ),
                    recommendation=(
                        "Keep only if the input is canonical and numeric; "
                        "do not parse the formatted output later."
                    ),
                )

            if (
                short_name in CALCULATION_FUNCTION_NAMES
                and contains_financial_term(
                    source_segment(self.source, node)
                )
            ):
                if is_assessment_policy_path(self.relative_path):
                    category = "FINANCIAL_DOMAIN_ARITHMETIC"
                    disposition = "ALLOWED_FINANCIAL_POLICY"
                    reason = (
                        "The calculation is contained in the explicit financial "
                        "assessment policy layer."
                    )
                    recommendation = (
                        "Keep the calculation centralized here and ensure its "
                        "inputs are canonical numeric metrics or validated series."
                    )
                elif (
                    short_name == "round"
                    and self.is_chart_context()
                ):
                    category = "DISPLAY_SCALING"
                    disposition = "ALLOWED_DISPLAY"
                    reason = (
                        "The operation appears to round a value for chart "
                        "or display presentation."
                    )
                    recommendation = (
                        "Confirm that the canonical source value remains "
                        "unchanged and that rounding affects display only."
                    )
                else:
                    category = "FINANCIAL_DOMAIN_ARITHMETIC"
                    disposition = "MUST_MIGRATE"
                    reason = (
                        "A calculation function is deriving or altering a "
                        "financially meaningful value."
                    )
                    recommendation = (
                        "Move this calculation into the canonical financial "
                        "metrics or assessment layer and consume the result."
                    )

                self.add(
                    node,
                    category=category,
                    symbol=function_name,
                    disposition=disposition,
                    reason=reason,
                    recommendation=recommendation,
                )

            if short_name in FORMATTED_VALUE_PARSERS:
                self.add(
                    node,
                    category="FORMATTED_VALUE_PARSING",
                    symbol=function_name,
                    disposition="MUST_MIGRATE",
                    reason=(
                        "Formatted presentation text is being converted back "
                        "into a financial number."
                    ),
                    recommendation=(
                        "Delete formatted-string parsing and consume raw "
                        "validated numeric values."
                    ),
                )

            if short_name in LEGACY_TABLE_EXTRACTORS:
                self.add(
                    node,
                    category="LEGACY_TABLE_EXTRACTION",
                    symbol=function_name,
                    disposition="MUST_MIGRATE",
                    reason=(
                        "Financial values are being recovered from a legacy "
                        "display table or statement representation."
                    ),
                    recommendation=(
                        "Replace display-table extraction with ValidatedMetric "
                        "or ValidatedSeries access."
                    ),
                )

        self.generic_visit(node)

    def visit_BinOp(
        self,
        node: ast.BinOp,
    ) -> None:
        expression = source_segment(
            self.source,
            node,
        )

        if (
            is_path_join_operation(node)
            or is_type_union_operation(node)
        ):
            self.generic_visit(node)
            return

        if self.is_layout_context():
            self.add(
                node,
                category="PAGE_LAYOUT_ARITHMETIC",
                symbol=node.op.__class__.__name__,
                disposition="ALLOWED_LAYOUT",
                reason=(
                    "The operation is performed in a PDF layout context and "
                    "controls page geometry rather than financial meaning."
                ),
                recommendation=(
                    "Keep as layout logic. Add a narrower explicit exclusion "
                    "only if future audit noise remains."
                ),
            )
        elif (
            self.is_chart_context()
            and contains_financial_term(expression)
            and is_display_scale_operation(node)
        ):
            self.add(
                node,
                category="DISPLAY_SCALING",
                symbol=node.op.__class__.__name__,
                disposition="ALLOWED_DISPLAY",
                reason=(
                    "The operation scales a financial value by a conventional "
                    "display unit inside chart/rendering code."
                ),
                recommendation=(
                    "Keep only as a display transformation. The chart must "
                    "receive canonical values and must not derive policy or "
                    "financial conclusions."
                ),
            )
        elif (
            contains_financial_term(expression)
            and is_assessment_policy_path(self.relative_path)
        ):
            self.add(
                node,
                category="FINANCIAL_DOMAIN_ARITHMETIC",
                symbol=node.op.__class__.__name__,
                disposition="ALLOWED_FINANCIAL_POLICY",
                reason=(
                    "The operation is contained in the explicit financial "
                    "assessment policy layer."
                ),
                recommendation=(
                    "Keep the policy centralized here and ensure inputs are "
                    "canonical numeric metrics or validated series."
                ),
            )
        elif contains_financial_term(expression):
            self.add(
                node,
                category="FINANCIAL_DOMAIN_ARITHMETIC",
                symbol=node.op.__class__.__name__,
                disposition="MUST_MIGRATE",
                reason=(
                    "The operation derives or changes a financially meaningful "
                    "number outside the canonical calculation or assessment "
                    "layer."
                ),
                recommendation=(
                    "Move the formula into services/analysis/"
                    "financial_metrics.py or analyst_assessment.py."
                ),
            )

        self.generic_visit(node)

    def visit_Compare(
        self,
        node: ast.Compare,
    ) -> None:
        expression = source_segment(
            self.source,
            node,
        )

        if (
            is_semantic_state_comparison(node)
            or is_status_comparison(node)
            or is_render_content_comparison(node)
            or is_availability_comparison(node)
        ):
            self.add(
                node,
                category="SEMANTIC_STATE_ROUTING",
                symbol="comparison",
                disposition="ALLOWED_SEMANTIC_ROUTING",
                reason=(
                    "The comparison selects narrative or rendering behavior "
                    "using semantic state or value availability."
                ),
                recommendation=(
                    "Keep routing here; ensure financial classifications are "
                    "derived in the canonical assessment layer."
                ),
            )
        elif (
            contains_financial_term(expression)
            and is_assessment_policy_path(self.relative_path)
        ):
            self.add(
                node,
                category="FINANCIAL_DOMAIN_ARITHMETIC",
                symbol="comparison",
                disposition="ALLOWED_FINANCIAL_POLICY",
                reason=(
                    "The comparison is contained in the explicit financial "
                    "assessment policy layer."
                ),
                recommendation=(
                    "Keep thresholds centralized here and document the policy "
                    "behind each classification boundary."
                ),
            )
        elif contains_financial_term(expression):
            self.add(
                node,
                category="FINANCIAL_DOMAIN_ARITHMETIC",
                symbol="comparison",
                disposition="MUST_MIGRATE",
                reason=(
                    "The layer applies a decision directly to financial "
                    "numbers or thresholds."
                ),
                recommendation=(
                    "Derive a semantic state in analyst_assessment.py and "
                    "route on that state instead."
                ),
            )

        self.generic_visit(node)


def audit_file(path: Path) -> list[AuditFinding]:
    source = path.read_text(encoding="utf-8")

    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [
            AuditFinding(
                file=str(path.relative_to(PROJECT_ROOT)),
                line=exc.lineno or 0,
                function="<module>",
                category="PARSE_ERROR",
                symbol="syntax_error",
                code=exc.msg,
                disposition="MUST_MIGRATE",
                reason="The file could not be parsed by the audit.",
                recommendation=(
                    "Fix or explicitly exclude this file before completing "
                    "the audit."
                ),
            )
        ]

    attach_parents(tree)

    visitor = ReportFinancialAuditVisitor(
        path=path,
        source=source,
    )
    visitor.visit(tree)

    return visitor.findings


def escape_markdown(value: str) -> str:
    return (
        value.replace("|", "\\|")
        .replace("\n", " ")
    )


def render_markdown(
    findings: list[AuditFinding],
) -> str:
    category_counts = Counter(
        finding.category
        for finding in findings
    )
    disposition_counts = Counter(
        finding.disposition
        for finding in findings
    )

    files_scanned = len(list(iter_python_files()))

    lines = [
        "# Veles Report Financial Path Audit",
        "",
        "## Objective",
        "",
        (
            "Identify financial-data access, legacy extraction, formatted-value "
            "parsing, financial-domain calculations, display transformations, "
            "semantic-state routing, and page-layout arithmetic in the report "
            "pipeline."
        ),
        "",
        "## Audit summary",
        "",
        f"- Files scanned: {files_scanned}",
        f"- Findings: {len(findings)}",
        "",
        "### Findings by category",
        "",
    ]

    for category, count in sorted(category_counts.items()):
        lines.append(f"- `{category}`: {count}")

    lines.extend(
        [
            "",
            "### Findings by disposition",
            "",
        ]
    )

    for disposition, count in sorted(disposition_counts.items()):
        lines.append(f"- `{disposition}`: {count}")

    lines.extend(
        [
            "",
            "## Classification model",
            "",
            "| Category | Meaning | Default disposition |",
            "|---|---|---|",
            (
                "| `FINANCIAL_DOMAIN_ARITHMETIC` | Creates a financial "
                "number, threshold result, sign, ratio, classification, or "
                "policy decision | `MUST_MIGRATE` outside canonical metrics "
                "and assessment; `ALLOWED_FINANCIAL_POLICY` inside the "
                "assessment layer |"
            ),
            (
                "| `DISPLAY_SCALING` | Converts canonical values into display "
                "units or display precision | `ALLOWED_DISPLAY` |"
            ),
            (
                "| `PAGE_LAYOUT_ARITHMETIC` | Controls PDF geometry, spacing, "
                "coordinates, or dimensions | `ALLOWED_LAYOUT` |"
            ),
            (
                "| `FORMATTING` | Converts canonical numeric values into "
                "presentation text | `ALLOWED_FORMATTING` |"
            ),
            (
                "| `SEMANTIC_STATE_ROUTING` | Chooses narrative or rendering "
                "from an already-derived state | "
                "`ALLOWED_SEMANTIC_ROUTING` |"
            ),
            (
                "| `DIRECT_DATA_ACCESS` | Navigates raw or normalized financial "
                "structures in the report/render layer | `MUST_MIGRATE` |"
            ),
            (
                "| `LEGACY_TABLE_EXTRACTION` | Recovers values from display "
                "tables or legacy statements | `MUST_MIGRATE` |"
            ),
            (
                "| `FORMATTED_VALUE_PARSING` | Parses presentation text back "
                "into numbers | `MUST_MIGRATE` |"
            ),
            "",
            "## Findings",
            "",
            (
                "| File | Line | Function | Category | Operation/path | "
                "Code | Disposition | Reason | Recommendation |"
            ),
            "|---|---:|---|---|---|---|---|---|---|",
        ]
    )

    for finding in sorted(
        findings,
        key=lambda item: (
            item.file,
            item.line,
            item.category,
        ),
    ):
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_markdown(finding.file),
                    str(finding.line),
                    escape_markdown(finding.function),
                    escape_markdown(finding.category),
                    escape_markdown(finding.symbol),
                    f"`{escape_markdown(finding.code)}`",
                    escape_markdown(finding.disposition),
                    escape_markdown(finding.reason),
                    escape_markdown(finding.recommendation),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Manual report-output inventory",
            "",
            (
                "Complete this table for every financial number, chart, table, "
                "ratio, and numerical narrative claim currently rendered."
            ),
            "",
            (
                "| Report output | Code location | Current source | "
                "Current calculation | Canonical target | Required period | "
                "Fallback behavior | Applicable companies | Status |"
            ),
            "|---|---|---|---|---|---|---|---|---|",
            (
                "| Share Price | | | | `share_price` | current market timestamp "
                "| withhold if unavailable | public equities | TODO |"
            ),
            (
                "| Market Capitalization | | | | `market_cap` | current market "
                "timestamp | withhold if unavailable | public equities | TODO |"
            ),
            (
                "| Cash & Equivalents | | | | "
                "`cash_and_cash_equivalents` | latest canonical balance-sheet "
                "date | withhold if unresolved | applicable issuers | TODO |"
            ),
            (
                "| Total Financial Debt | | | | `financial_debt` | same "
                "balance-sheet date as cash | withhold if incomplete | "
                "nonfinancial operating companies | TODO |"
            ),
            (
                "| Reconciled Enterprise Value | | | | "
                "`reconciled_enterprise_value` | current market timestamp plus "
                "canonical balance-sheet date | withhold if debt incomplete | "
                "applicable issuers | TODO |"
            ),
            (
                "| Revenue History | | | | validated annual revenue series | "
                "fiscal annual periods | withhold invalid periods | "
                "applicable issuers | TODO |"
            ),
            (
                "| R&D History | | | | validated annual R&D series | fiscal "
                "annual periods | omit when inapplicable/unresolved | "
                "applicable issuers | TODO |"
            ),
            (
                "| Operating Income/Loss | | | | validated operating-income "
                "series | fiscal annual periods | withhold invalid periods | "
                "applicable issuers | TODO |"
            ),
            (
                "| Net Income/Loss | | | | validated net-income series | fiscal "
                "annual periods | withhold invalid periods | "
                "applicable issuers | TODO |"
            ),
            (
                "| Operating Cash Flow | | | | validated operating-cash-flow "
                "series | fiscal annual periods | withhold invalid periods | "
                "applicable issuers | TODO |"
            ),
            (
                "| Capital Expenditures | | | | validated capex series | fiscal "
                "annual periods | withhold invalid periods | "
                "applicable issuers | TODO |"
            ),
            (
                "| Free Cash Flow | | | | canonical calculated metric | same "
                "period for OCF and capex | withhold incomplete inputs | "
                "applicable issuers | TODO |"
            ),
            (
                "| Cash Runway | | | | canonical runway metric | balance-sheet "
                "cash and compatible burn period | withhold when burn is not "
                "meaningful | cash-burning companies | TODO |"
            ),
            (
                "| Revenue Growth | | | | validated growth series | comparable "
                "annual periods | withhold incomparable periods | "
                "revenue-reporting issuers | TODO |"
            ),
            "",
            "## Exit criteria",
            "",
            (
                "- Every existing report financial output appears in the "
                "manual inventory."
            ),
            (
                "- Every finding has a category, disposition, reason, and "
                "recommended architectural action."
            ),
            (
                "- `MUST_MIGRATE` is reserved for financial-domain logic, raw "
                "access, formatted-value parsing, and legacy extraction."
            ),
            (
                "- Display scaling, formatting, semantic routing, and layout "
                "arithmetic remain allowed only inside their proper layers."
            ),
            (
                "- No financial result lacks a canonical target and period rule."
            ),
            "",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    findings: list[AuditFinding] = []

    for path in iter_python_files():
        findings.extend(audit_file(path))

    OUTPUT_PATH.write_text(
        render_markdown(findings),
        encoding="utf-8",
    )

    category_counts = Counter(
        finding.category
        for finding in findings
    )
    disposition_counts = Counter(
        finding.disposition
        for finding in findings
    )

    print(f"Audit written to: {OUTPUT_PATH}")
    print(f"Findings: {len(findings)}")

    print("\nCategories:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count}")

    print("\nDispositions:")
    for disposition, count in sorted(disposition_counts.items()):
        print(f"  {disposition}: {count}")

    print("\nDetailed findings:")
    for finding in findings:
        print(
            f"{finding.file}:{finding.line} "
            f"[{finding.category}] "
            f"[{finding.disposition}] "
            f"{finding.function}: {finding.symbol}"
        )


if __name__ == "__main__":
    main()
