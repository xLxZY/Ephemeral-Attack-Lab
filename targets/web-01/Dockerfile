FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        openssh-server nginx postgresql postgresql-contrib \
        python3 python3-pip python3-venv python3-dev \
        cron sudo iproute2 procps curl ca-certificates \
        libpq5 libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /run/sshd

RUN useradd -m -s /bin/bash deploy \
    && useradd -m -s /bin/bash analyst \
    && mkdir -p /home/backup \
    && usermod -d /home/backup -s /bin/bash backup \
    && chown backup:backup /home/backup \
    && echo 'deploy:AcmeR3port-91' | chpasswd \
    && echo 'analyst:AcmeR3port-92' | chpasswd \
    && echo 'backup:AcmeR3port-93' | chpasswd

RUN mkdir -p \
      /opt/acme-reporting/app \
      /opt/acme-reporting/config \
      /opt/acme-reporting/scripts \
      /opt/acme-reporting/logs \
      /opt/acme-reporting/backups \
      /var/log/acme-reporting

COPY app/ /opt/acme-reporting/app/
COPY config/nginx-acme.conf /etc/nginx/sites-available/acme
COPY config/sshd_config /opt/acme-reporting/config-sshd
COPY config/init-db.sql /opt/acme-reporting/init-db.sql
COPY config/pg_hba_extra.conf /opt/acme-reporting/pg_hba_extra.conf
COPY config/crontab.root /opt/acme-reporting/crontab.root
COPY config/crontab.backup /opt/acme-reporting/crontab.backup
COPY scripts/deploy-hook.sh /opt/acme-reporting/scripts/deploy-hook.sh
COPY scripts/backup.sh /opt/acme-reporting/scripts/backup.sh
COPY scripts/healthcheck.sh /opt/acme-reporting/scripts/healthcheck.sh
COPY scripts/noise.sh /opt/acme-reporting/scripts/noise.sh
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN rm -f /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/acme /etc/nginx/sites-enabled/acme \
    && python3 -m venv /opt/acme-reporting/venv \
    && /opt/acme-reporting/venv/bin/pip install --no-cache-dir -r /opt/acme-reporting/app/requirements.txt \
    && chown -R deploy:deploy /opt/acme-reporting \
    && chown backup:backup /opt/acme-reporting/backups \
    && chmod 755 /opt/acme-reporting/scripts/*.sh /usr/local/bin/entrypoint.sh \
    && chmod 775 /opt/acme-reporting/scripts/deploy-hook.sh \
    && chown deploy:deploy /opt/acme-reporting/scripts/deploy-hook.sh \
    && chmod 755 /opt/acme-reporting/scripts/backup.sh \
    && chown backup:backup /opt/acme-reporting/scripts/backup.sh \
    && chown -R deploy:deploy /var/log/acme-reporting \
    && chmod 755 /home/analyst /home/backup /home/deploy

EXPOSE 22 80
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
