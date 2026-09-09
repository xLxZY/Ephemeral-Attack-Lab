# Appendix

## A — Technology justification

Docker: reproducible isolated environments. Terraform: lab lifecycle as code. Python: orchestration. Elasticsearch: searchable events. Grafana: investigation. nmap: discovery. hydra: lab authentication testing.

## B — Configuration

MAX_ACTIVE_LABS, LAB_DEFAULT_DURATION, ELASTICSEARCH_URL, GRAFANA_URL, DOCKER_NETWORK_RANGE, CYBERLAB_DATA_DIR, CYBERLAB_REPORTS_DIR.

## C — Attacker tools

nmap, netcat, iproute2, dnsutils, hydra, openssh-client, curl, wget, jq, python3, bash, git, vim, procps. Installed via apt in attacker/Dockerfile. Scenario: ssh-privesc.

## D — Target services

Nginx (front door), Flask app (reporting), PostgreSQL (data), SSH (admin access), cron (jobs), backup.sh, logging under /var/log/acme-reporting.

## E — Example lab

lab-001, ssh-privesc, 172.20.0.0/24, attacker 172.20.0.2, target 172.20.0.3.

## F — Example evidence

{"lab_id":"lab-001","event_type":"authentication_failure","host":"web-01"}

## G — Testing results

Fill after you run the demo: create, attacker, target, isolation, telemetry, ES, Grafana, evidence, destroy, recreate.
