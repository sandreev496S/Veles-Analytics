import importlib
import sys

import pytest


def test_ai_memo_imports_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    sys.modules.pop("services.ai_memo", None)
    module = importlib.import_module("services.ai_memo")
    assert callable(module.generate_investment_memo)


def test_client_is_created_lazily(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    from services import ai_memo

    with pytest.raises(RuntimeError, match="AI memo generation"):
        ai_memo._get_openai_client()
