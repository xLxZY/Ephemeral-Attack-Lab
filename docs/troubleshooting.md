# Troubleshooting

Docker no Server: systemctl start docker; re-login for docker group.

Target exits: docker logs web-01-<lab>; entrypoint must reach sleep infinity.

Health check fail: wait for postgres; curl from attacker to target IP.

Subnet in use: docker network ls; destroy leftover cyberlab-* networks.

ES dies: RAM; vm.max_map_count; ES_JAVA_OPTS.

Grafana empty: time range UTC; run cyberlab collect; confirm curl localhost:9200/cyberlab-events/_count.

Destroy leftover: terraform destroy with the lab state file under ~/.cyberlab/labs/<id>/.

Orphans: docker ps -a --filter label=cyberlab=true; docker network ls.
