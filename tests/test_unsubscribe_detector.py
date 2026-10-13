#!/usr/bin/env python3
"""Unit tests for unsubscribe link extraction and URL safety."""

import re

from config.keywords import UNSUBSCRIBE_PATTERNS
from core.unsubscribe_detector import UnsubscribeDetector


def test_unsubscribe_patterns_compile():
    """All configured unsubscribe regexes should compile cleanly."""
    for pattern in UNSUBSCRIBE_PATTERNS:
        re.compile(pattern)


def test_safe_unsubscribe_url_allows_expected_schemes():
    detector = UnsubscribeDetector()

    assert detector.is_safe_unsubscribe_url("https://example.com/unsubscribe?id=123")
    assert detector.is_safe_unsubscribe_url("http://example.com/unsubscribe")
    assert detector.is_safe_unsubscribe_url("mailto:unsubscribe@example.com")


def test_safe_unsubscribe_url_rejects_unsafe_schemes_and_empty_values():
    detector = UnsubscribeDetector()

    assert not detector.is_safe_unsubscribe_url("javascript:alert('unsubscribe')")
    assert not detector.is_safe_unsubscribe_url("data:text/html,unsubscribe")
    assert not detector.is_safe_unsubscribe_url("file:///tmp/unsubscribe.html")
    assert not detector.is_safe_unsubscribe_url("")


def test_extract_unsubscribe_links_from_html_and_plain_text():
    detector = UnsubscribeDetector()
    content = """
    <html>
      <body>
        <a href="https://news.example.com/unsubscribe?token=abc123">unsubscribe</a>
        List-Unsubscribe: <mailto:unsubscribe@example.com>
        unsubscribe: https://example.org/unsubscribe/preferences
      </body>
    </html>
    """

    links = detector.extract_unsubscribe_links(content)

    assert "https://news.example.com/unsubscribe?token=abc123" in links
    assert "https://example.org/unsubscribe/preferences" in links
    assert any(link.startswith("mailto:unsubscribe@example.com") for link in links)


def test_extract_unsubscribe_links_filters_unsafe_matches():
    detector = UnsubscribeDetector()
    content = """
    <a href="javascript:unsubscribeUser()">bad</a>
    <a href="file:///tmp/unsubscribe.html">also bad</a>
    <a href="https://safe.example/unsubscribe">good</a>
    """

    links = detector.extract_unsubscribe_links(content)

    assert links == ["https://safe.example/unsubscribe"]


def test_extract_unsubscribe_links_deduplicates_and_handles_empty_content():
    detector = UnsubscribeDetector()
    content = (
        '<a href="https://example.com/unsubscribe">unsubscribe</a> '
        'https://example.com/unsubscribe'
    )

    assert detector.extract_unsubscribe_links(content).count(
        "https://example.com/unsubscribe"
    ) == 1
    assert detector.extract_unsubscribe_links("No opt-out link here") == []
