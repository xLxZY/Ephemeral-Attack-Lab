# Development

Package lives in src/cyberlab. Install editable: pip install -e ".[dev]".

New scenario: directory under scenarios/<name>/scenario.yaml and loader must find it; add images only if needed.

Tests: pytest unit tests for duration, subnet, yaml, events.

Do not add Kubernetes, Kafka, Redis, Prometheus, or extra scenarios before the first loop is done.
