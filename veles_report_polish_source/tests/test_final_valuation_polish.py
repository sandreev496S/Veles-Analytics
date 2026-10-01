from services.valuation.valuation_report_adapter import (
    _build_review_flags,
)


def test_review_flags_include_monotonicity():
    payload = {
        "model_status": "illustrative",
    }

    base = {
        "assumptions": {
            "cash": 200,
            "debt": 50,
        },
        "forecast": [
            {
                "year": 2030,
                "ebit": -10,
                "ebit_margin": -0.10,
            },
            {
                "year": 2031,
                "ebit": 20,
                "ebit_margin": 0.45,
            },
        ],
    }

    scenarios = {
        "bull": {
            "implied_value_per_share": 15,
        },
        "base": {
            "implied_value_per_share": 10,
        },
        "bear": {
            "implied_value_per_share": 4,
        },
    }

    flags = _build_review_flags(
        payload,
        base,
        scenarios,
        [],
    )

    items = [
        flag["item"]
        for flag in flags
    ]

    assert any(
        "Scenario monotonicity passed"
        in item
        for item in items
    )

    assert any(
        "positive EBIT in 2031"
        in item
        for item in items
    )

    assert any(
        "net-cash balance"
        in item
        for item in items
    )


def test_review_flags_detect_high_terminal_margin():
    flags = _build_review_flags(
        {
            "model_status": "illustrative",
        },
        {
            "assumptions": {
                "cash": 100,
                "debt": 20,
            },
            "forecast": [
                {
                    "year": 2040,
                    "ebit": 100,
                    "ebit_margin": 0.636,
                }
            ],
        },
        {
            "bull": {
                "implied_value_per_share": 12,
            },
            "base": {
                "implied_value_per_share": 8,
            },
            "bear": {
                "implied_value_per_share": 0,
            },
        },
        [],
    )

    assert any(
        "exceeds 40%"
        in flag["item"]
        for flag in flags
    )


def test_review_flags_deduplicate_semantic_warnings():
    flags = _build_review_flags(
        {
            "model_status": "illustrative",
        },
        {
            "assumptions": {
                "cash": 200,
                "debt": 50,
            },
            "forecast": [
                {
                    "year": 2033,
                    "ebit": -10,
                    "ebit_margin": -0.03,
                },
                {
                    "year": 2034,
                    "ebit": 100,
                    "ebit_margin": 0.636,
                },
            ],
        },
        {
            "bull": {
                "implied_value_per_share": 17.0,
            },
            "base": {
                "implied_value_per_share": 8.0,
            },
            "bear": {
                "implied_value_per_share": 0.0,
            },
        },
        [
            "This is an illustrative scenario model, not a final valuation.",
            (
                "Terminal-year EBIT margin exceeds 40%. "
                "Review mature-state revenue and operating-expense assumptions."
            ),
        ],
    )

    categories = [
        flag["category"]
        for flag in flags
    ]

    assert categories.count("illustrative_model") == 1
    assert categories.count("terminal_margin") == 1
    assert len(flags) == 5
