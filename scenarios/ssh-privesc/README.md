# ssh-privesc

Objective: controlled lab exercise against web-01 from attacker-01.

Environment: isolated Docker network, no published ports.

Services: SSH, Nginx, Flask, PostgreSQL, cron, backup.

Attacker tools: nmap, hydra, netcat, ssh, curl, python3.

Initial conditions: lab users exist; deploy-hook.sh is writable by deploy and run by root cron; background jobs generate logs.

Expected progression (high level): recon → service discovery → lab authentication testing → SSH as low-privilege user → local enumeration → operational weakness → elevated privileges.

Telemetry: authentication, process (deploy-hook/backup/cron), HTTP/network via nginx.

Cleanup: cyberlab destroy collects evidence first.
