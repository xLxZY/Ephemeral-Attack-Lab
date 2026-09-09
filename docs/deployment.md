# Deployment (clean Ubuntu VM)

1. Install Git, Python 3, Docker Engine, Terraform (see walkthrough section 0).
2. Clone or copy this repository.
3. `cp .env.example .env`
4. `docker build -t cyberlab-web-01:dev ./targets/web-01`
5. `docker build -t cyberlab-attacker:dev ./attacker`
6. `sudo sysctl -w vm.max_map_count=262144`
7. `docker compose -f infrastructure/platform/docker-compose.yml up -d`
8. `cd infrastructure/terraform && terraform init && cd ../..`
9. `python3 -m venv .venv && source .venv/bin/activate && pip install -e .`
10. `cyberlab create --scenario ssh-privesc`
11. `cyberlab shell attacker <lab-id>`
12. Exercise only the lab target IP; then `cyberlab collect <lab-id>` and `cyberlab report <lab-id>`
13. `cyberlab destroy <lab-id>`

Optional expiry worker:

* * * * * cd $HOME/Projects/ephemeral-attack-lab && $HOME/Projects/ephemeral-attack-lab/.venv/bin/cyberlab reap
