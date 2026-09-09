FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        nmap netcat-openbsd iproute2 dnsutils hydra openssh-client \
        curl wget jq python3 bash git \
        grep sed gawk less procps vim-tiny ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash analyst \
    && mkdir -p /home/analyst/tools /home/analyst/scripts /home/analyst/workspace /home/analyst/notes /home/analyst/wordlists \
    && chown -R analyst:analyst /home/analyst

COPY wordlists/custom-1000.txt /home/analyst/wordlists/custom-1000.txt
RUN chown analyst:analyst /home/analyst/wordlists/custom-1000.txt

COPY config/motd /etc/motd
COPY scripts/README /home/analyst/scripts/README
RUN chown analyst:analyst /home/analyst/scripts/README

USER analyst
WORKDIR /home/analyst
CMD ["sleep", "infinity"]
