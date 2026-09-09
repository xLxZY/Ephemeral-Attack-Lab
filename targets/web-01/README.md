# web-01

Acme Analytics internal reporting server.

Services: Nginx, Flask app, PostgreSQL, SSH, cron, backups.
Users: deploy (app + writable deploy-hook), analyst (read-oriented), backup (backup job).

Operational weakness: `/opt/acme-reporting/scripts/deploy-hook.sh` is writable by `deploy` and executed by root cron.

Lab SSH passwords (isolated lab only): deploy/labdeploy, analyst/labanalyst, backup/labbackup.
