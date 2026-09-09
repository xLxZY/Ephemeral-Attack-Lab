# Security

Threat model: keep a lab exercise from reaching the hypervisor host or LAN.

Controls: internal Docker network, no published ports, no docker.sock, no privileged, no host mounts, memory/CPU limits, MAX_ACTIVE_LABS, short duration, ES/Grafana on 127.0.0.1.

Lab passwords (VM lab only): deploy/labdeploy, analyst/labanalyst, backup/labbackup. Grafana admin/labgrafana. Postgres acme/acme_lab_db.

Limitations: Docker breakout is out of scope; still avoid socket and privileged. Elasticsearch security is off on the private VM.

Cleanup: destroy collects evidence first; reports/ is not deleted.
