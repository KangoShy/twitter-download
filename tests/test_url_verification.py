# Assuming all url arguments are standard twitter media url's.

import pytest
from urllib.parse import urlparse


@pytest.mark.unit
def test_domain_valid():
    """Assert the site is equal to twitter.com"""
    url = "https://twitter.com/TrollFootball/status/1679583964770754560?s=20"

    parsed_url = urlparse(url)

    assert parsed_url.hostname == "twitter.com"
