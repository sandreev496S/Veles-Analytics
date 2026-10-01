from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest


FIXTURES = Path(__file__).parent / "fixtures"
SNAPSHOTS = Path(__file__).parent / "snapshots"


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--run-live",
        action="store_true",
        default=False,
        help="run tests marked live_provider that may access external services",
    )


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    if config.getoption("--run-live"):
        return
    skip_live = pytest.mark.skip(reason="requires --run-live and external provider access")
    for item in items:
        if "live_provider" in item.keywords:
            item.add_marker(skip_live)


@pytest.fixture
def load_fixture():
    def _load(relative_path: str) -> Any:
        with (FIXTURES / relative_path).open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return _load


@pytest.fixture
def assert_json_snapshot():
    def _assert(name: str, actual: Any) -> None:
        path = SNAPSHOTS / name
        expected = json.loads(path.read_text(encoding="utf-8"))
        assert actual == expected
    return _assert
