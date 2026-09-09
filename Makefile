.PHONY: venv build-attacker build-target platform-up platform-down test

venv:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -U pip && pip install -e ".[dev]"

build-target:
	docker build -t cyberlab-web-01:dev ./targets/web-01

build-attacker:
	docker build -t cyberlab-attacker:dev ./attacker

platform-up:
	docker compose -f infrastructure/platform/docker-compose.yml up -d

platform-down:
	docker compose -f infrastructure/platform/docker-compose.yml down

test:
	. .venv/bin/activate && pytest -q
