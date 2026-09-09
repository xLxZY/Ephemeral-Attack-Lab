#!/bin/bash
# Intentional lab misconfiguration: this file is writable by deploy and executed by root cron.
set -u
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "${ts} deploy-hook host=$(hostname) user=$(id -un) uid=$(id -u)" >> /var/log/acme-reporting/deploy-hook.log
