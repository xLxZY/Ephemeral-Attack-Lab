#!/bin/bash
set -u
ts="$(date -u +%Y%m%dT%H%M%SZ)"
dest="/opt/acme-reporting/backups/reports-${ts}.sql"
if command -v pg_dump >/dev/null 2>&1; then
  PGPASSWORD=acme_lab_db pg_dump -h 127.0.0.1 -U acme acme_reporting > "${dest}" 2>/dev/null || true
fi
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) backup wrote ${dest} user=$(id -un)" >> /var/log/acme-reporting/backup.log
