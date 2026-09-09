# Telemetry

Event fields: lab_id, timestamp, host, event_type, plus optional source, user, process, command, severity, metadata.

Index: cyberlab-events

Ship path: docker exec read of auth.log, nginx access.log, deploy-hook.log, backup.log → JSONL under ~/.cyberlab/labs/<id>/events.jsonl → Elasticsearch _bulk.

Command: cyberlab collect <lab-id>
