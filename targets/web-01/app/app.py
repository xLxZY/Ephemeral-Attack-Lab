#!/usr/bin/env python3
import os
import datetime
from flask import Flask, render_template
import psycopg2

app = Flask(__name__)
LOG = "/var/log/acme-reporting/app.log"
DSN = os.environ.get(
    "ACME_DSN",
    "host=127.0.0.1 dbname=acme_reporting user=acme password=acme_lab_db",
)


def log(msg: str) -> None:
    ts = datetime.datetime.now(datetime.timezone.utc).isoformat()
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as fh:
        fh.write(f"{ts} {msg}\n")


def report_count() -> int:
    try:
        conn = psycopg2.connect(DSN)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM reports")
        n = int(cur.fetchone()[0])
        cur.close()
        conn.close()
        return n
    except Exception as exc:
        log(f"db_error {exc}")
        return -1


@app.get("/")
def index():
    n = report_count()
    log("http_index")
    return render_template("index.html", count=n)


@app.get("/health")
def health():
    n = report_count()
    log("http_health")
    status = "ok" if n >= 0 else "degraded"
    return {"status": status, "reports": n}


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
