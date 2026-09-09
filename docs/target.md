# Target web-01

Role: Acme Analytics internal reporting server.

Filesystem: /opt/acme-reporting/{app,config,scripts,logs,backups}, /var/log/acme-reporting, /home/{deploy,analyst,backup}

Users: deploy (application + deploy-hook), analyst (read/report), backup (backup.sh).

Weakness: deploy-hook.sh writable by deploy, executed every minute as root via cron.

Reset: destroy container; image rebuild is the source of truth.

Network: only the lab bridge; no published ports.
