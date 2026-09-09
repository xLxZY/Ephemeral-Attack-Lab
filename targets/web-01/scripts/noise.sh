#!/bin/bash
curl -sS -o /dev/null http://127.0.0.1/ || true
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) noise curl_index" >> /var/log/acme-reporting/noise.log
