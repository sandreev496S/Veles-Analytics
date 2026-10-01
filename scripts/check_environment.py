#!/usr/bin/env python3
"""Preflight checks for the Veles Streamlit application.

Run with:
    python scripts/check_environment.py

The script does not import the application itself, so it can report missing
packages and configuration cleanly instead of failing during Streamlit startup.
"""
from __future__ import annotations

import importlib
import os
import platform
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    load_dotenv = None


ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class CheckResult:
    name: str
    ok: bool
    detail: str
    required: bool = True


PACKAGES: tuple[tuple[str, str], ...] = (
    ("streamlit", "streamlit"),
    ("pandas", "pandas"),
    ("numpy", "numpy"),
    ("plotly", "plotly"),
    ("matplotlib", "matplotlib"),
    ("openpyxl", "openpyxl"),
    ("xlsxwriter", "XlsxWriter"),
    ("xlrd", "xlrd"),
    ("reportlab", "reportlab"),
    ("yfinance", "yfinance"),
    ("openai", "openai"),
    ("dotenv", "python-dotenv"),
    ("requests", "requests"),
    ("sqlalchemy", "SQLAlchemy"),
    ("psycopg2", "psycopg2-binary"),
    ("supabase", "supabase"),
    ("sentry_sdk", "sentry-sdk"),
)

PRODUCTION_ENV_VARS = (
    "SUPABASE_URL",
    "SUPABASE_ANON_KEY",
    "SUPABASE_SERVICE_ROLE_KEY",
    "DATABASE_URL",
)


def check_python() -> CheckResult:
    current = sys.version_info
    ok = current >= (3, 11) and current < (3, 14)
    detail = f"{platform.python_version()} ({sys.executable})"
    if not ok:
        detail += "; use Python 3.11–3.13 (3.12 recommended)"
    return CheckResult("Python", ok, detail)


def check_package(module_name: str, package_name: str) -> CheckResult:
    try:
        module = importlib.import_module(module_name)
        version = getattr(module, "__version__", None)
        detail = f"installed{f' ({version})' if version else ''}"
        return CheckResult(package_name, True, detail)
    except Exception as exc:  # includes broken binary/import installations
        return CheckResult(
            package_name,
            False,
            f"unavailable: {exc.__class__.__name__}: {exc}",
        )


def check_project_files() -> Iterable[CheckResult]:
    for relative in ("app.py", "requirements.txt", ".streamlit/config.toml"):
        path = ROOT / relative
        yield CheckResult(relative, path.exists(), "present" if path.exists() else "missing")


def check_writable_directory(relative: str) -> CheckResult:
    path = ROOT / relative
    try:
        path.mkdir(parents=True, exist_ok=True)
        probe = path / ".veles_write_test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        return CheckResult(relative, True, f"writable ({path})")
    except OSError as exc:
        return CheckResult(relative, False, f"not writable: {exc}")


def check_configuration() -> list[CheckResult]:
    if load_dotenv is not None:
        load_dotenv(ROOT / ".env")

    mode = os.getenv("APP_MODE", "demo").strip().lower()
    results = [
        CheckResult(
            "APP_MODE",
            mode in {"demo", "production"},
            mode if mode in {"demo", "production"} else f"invalid value: {mode!r}",
        )
    ]

    if mode == "production":
        for variable in PRODUCTION_ENV_VARS:
            value = os.getenv(variable, "").strip()
            results.append(
                CheckResult(variable, bool(value), "configured" if value else "missing")
            )
        openai_value = os.getenv("OPENAI_API_KEY", "").strip()
        results.append(
            CheckResult(
                "OPENAI_API_KEY",
                bool(openai_value),
                "configured" if openai_value else "missing (AI commentary disabled)",
                required=False,
            )
        )
    else:
        results.append(CheckResult("Cloud services", True, "not required in demo mode", required=False))

    return results


def print_result(result: CheckResult) -> None:
    symbol = "✓" if result.ok else ("!" if not result.required else "✗")
    label = "optional" if not result.required else "required"
    print(f"{symbol} {result.name:<28} {result.detail} [{label}]")


def main() -> int:
    print("=" * 72)
    print("VELES ENVIRONMENT CHECK")
    print("=" * 72)

    results: list[CheckResult] = [check_python()]
    results.extend(check_package(module, package) for module, package in PACKAGES)
    results.extend(check_project_files())
    results.append(check_writable_directory("data"))
    results.append(check_writable_directory("output"))
    results.extend(check_configuration())

    for result in results:
        print_result(result)

    failures = [r for r in results if r.required and not r.ok]
    print("-" * 72)
    if failures:
        print(f"Environment is not ready: {len(failures)} required check(s) failed.")
        print("Repair command:")
        print(f'  "{sys.executable}" -m pip install -r "{ROOT / "requirements.txt"}"')
        return 1

    print("Environment ready. Start Veles with:")
    print(f'  "{sys.executable}" -m streamlit run "{ROOT / "app.py"}"')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
