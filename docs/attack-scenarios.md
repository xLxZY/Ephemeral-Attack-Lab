# Attack scenarios

## ssh-privesc

- Name: ssh-privesc
- Objective: controlled access path using the lab’s operational weakness
- Environment: attacker-01 → lab network → web-01
- Services: nginx, ssh, postgres, cron, backup
- Tools on attacker: nmap, hydra, netcat, ssh, curl, python
- Initial conditions: documented lab users; writable deploy-hook executed by root cron; background noise
- Expected progression: recon, discovery, lab authentication testing, SSH, enumeration, weakness, elevation
- Telemetry: auth, process, HTTP
- Final state: investigator can explain the timeline from evidence
- Evidence: reports/<lab-id>/
- Cleanup: cyberlab destroy
