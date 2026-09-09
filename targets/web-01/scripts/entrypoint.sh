#!/bin/bash
set -euo pipefail

mkdir -p /var/log/acme-reporting /opt/acme-reporting/backups /run/sshd
chown -R deploy:deploy /var/log/acme-reporting /opt/acme-reporting/logs || true
touch /var/log/acme-reporting/app.log /var/log/acme-reporting/access.log \
      /var/log/acme-reporting/security.log /var/log/acme-reporting/cron.log
chmod 666 /var/log/acme-reporting/*.log || true

if [[ ! -f /etc/ssh/ssh_host_rsa_key ]]; then
  ssh-keygen -A
fi
cp /opt/acme-reporting/config-sshd /etc/ssh/sshd_config
chmod 600 /etc/ssh/sshd_config

PG_VER="$(ls /etc/postgresql | head -n1)"
PG_CONF="/etc/postgresql/${PG_VER}/main/postgresql.conf"
PG_HBA="/etc/postgresql/${PG_VER}/main/pg_hba.conf"
sed -i "s/^#\\?listen_addresses.*/listen_addresses = 'localhost'/" "${PG_CONF}"
if ! grep -q "acme_reporting acme" "${PG_HBA}"; then
  cat /opt/acme-reporting/pg_hba_extra.conf >> "${PG_HBA}"
fi

pg_ctlcluster "${PG_VER}" main start
sleep 2

if ! sudo -u postgres psql -tAc "SELECT 1 FROM pg_roles WHERE rolname='acme'" | grep -q 1; then
  sudo -u postgres psql -v ON_ERROR_STOP=1 -f /opt/acme-reporting/init-db.sql
fi

crontab /opt/acme-reporting/crontab.root
crontab -u backup /opt/acme-reporting/crontab.backup
cron

/usr/sbin/sshd

sudo -u deploy env ACME_DSN="host=127.0.0.1 dbname=acme_reporting user=acme password=acme_lab_db" \
  /opt/acme-reporting/venv/bin/python /opt/acme-reporting/app/app.py \
  >> /var/log/acme-reporting/app.log 2>&1 &

nginx
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) web-01 entrypoint ready lab=${LAB_ID:-unknown}" >> /var/log/acme-reporting/app.log

exec sleep infinity
