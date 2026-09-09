# Attacker

Purpose: reproducible security workstation, user analyst, hostname attacker-01.

Layout: /home/analyst/{tools,scripts,workspace,notes}

| Tool | Why |
|---|---|
| nmap | service discovery |
| hydra | lab-only authentication testing |
| netcat | connectivity checks |
| ssh | lab remote access |
| curl/wget/jq | HTTP |
| python3/bash/git | scripting |

Enter: `cyberlab shell attacker <lab-id>`

Boundary: internal Docker network, no docker.sock, no privileged, no host FS, no host network.

Add tools only when a new scenario needs them.
