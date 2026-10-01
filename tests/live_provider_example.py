"""Template for optional provider smoke tests.

Move an existing live-provider assertion here only when it genuinely needs network
access, then run it explicitly with: pytest --run-live -m live_provider
"""

import pytest

pytestmark = pytest.mark.live_provider


@pytest.mark.skip(reason="template: replace with a real provider smoke assertion")
def test_live_provider_smoke_template():
    pass
