import pytest
from ai_review import build_review_request, review_notes


def test_request_keeps_notes_separate():
    messages = build_review_request("Warm vocal", "Clear bass")
    assert len(messages) == 2
    assert "Warm vocal" in messages[1]["content"]
    assert "Clear bass" in messages[1]["content"]
    assert "Do not claim to have listened" in messages[0]["content"]


def test_empty_notes_rejected():
    with pytest.raises(ValueError):
        build_review_request("", "Good arrangement")


def test_long_notes_rejected():
    with pytest.raises(ValueError):
        build_review_request("a" * 4001, "Good arrangement")


def test_key_required_before_network():
    with pytest.raises(ValueError):
        review_notes("a", "b", "")
