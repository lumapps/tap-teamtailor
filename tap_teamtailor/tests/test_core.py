"""Tests standard tap features using the built-in SDK tests library."""
from singer_sdk.testing import get_standard_tap_tests

from tap_teamtailor.tap import Tapteamtailor

SAMPLE_CONFIG = {
    "api_key": "the-api-key"
}


# Run standard built-in tap tests from the SDK:
def test_standard_tap_tests():
    """Run standard tap tests from the SDK."""
    tests = get_standard_tap_tests(
        Tapteamtailor,
        config=SAMPLE_CONFIG
    )
    for test in tests:
        test()
