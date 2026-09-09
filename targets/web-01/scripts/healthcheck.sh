#!/bin/bash
code="$(curl -sS -o /dev/null -w '%{http_code}' http://127.0.0.1/health || echo 000)"
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) health http=${code}" >> /var/log/acme-reporting/health.log
