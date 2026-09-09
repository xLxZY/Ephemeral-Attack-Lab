from cyberlab.telemetry.events import make_event


def test_required_fields():
    e = make_event("lab-001", "web-01", "http_request")
    assert e["lab_id"] == "lab-001"
    assert e["host"] == "web-01"
    assert e["event_type"] == "http_request"
    assert "timestamp" in e
