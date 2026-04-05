"""
GreenPulse sensor emulator: publishes random precision-agriculture telemetry as JSON.
"""
from __future__ import annotations

import json
import os
import sys
import time

import requests

from telemetry_logic import sample_telemetry

INGEST_URL = os.environ.get("INGEST_URL", "http://localhost:8080/api/v1/telemetry")
INTERVAL = float(os.environ.get("EMULATOR_INTERVAL_SECONDS", "5"))
PLOT_ID = os.environ.get("PLOT_ID", "plot-local-01")


def main() -> None:
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    print(f"Emitting telemetry every {INTERVAL}s to {INGEST_URL}", flush=True)
    while True:
        payload = sample_telemetry(PLOT_ID)
        try:
            r = session.post(INGEST_URL, data=json.dumps(payload), timeout=10)
            if r.ok:
                print(f"OK {r.status_code} {payload}", flush=True)
            else:
                print(f"ERR {r.status_code} {r.text}", flush=True)
        except requests.RequestException as exc:
            print(f"request failed: {exc}", flush=True)
        time.sleep(INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
