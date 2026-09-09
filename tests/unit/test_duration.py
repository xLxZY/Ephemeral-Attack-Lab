from datetime import timedelta

from cyberlab.orchestrator.duration import parse_duration


def test_parse_minutes():
    assert parse_duration("30m") == timedelta(minutes=30)


def test_parse_hours():
    assert parse_duration("1h") == timedelta(hours=1)
