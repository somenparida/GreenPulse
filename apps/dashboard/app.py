"""
GreenPulse Streamlit dashboard: crop health visualization from ingestion API.
"""
from __future__ import annotations

import os
import time

import pandas as pd
import requests
import streamlit as st

API = os.environ.get("INGESTION_API_URL", "http://localhost:8080")
REFRESH = float(os.environ.get("DASHBOARD_REFRESH_SECONDS", "10"))


@st.cache_data(ttl=5)
def fetch_readings(limit: int = 200) -> list:
    url = f"{API.rstrip('/')}/api/v1/readings"
    r = requests.get(url, params={"limit": limit}, timeout=15)
    r.raise_for_status()
    return r.json()


def main() -> None:
    st.set_page_config(page_title="GreenPulse", layout="wide")
    st.title("GreenPulse — Precision Agriculture")
    st.caption("Live telemetry: moisture, temperature, pH")

    try:
        data = fetch_readings()
    except requests.RequestException as exc:
        st.error(f"Could not reach ingestion API at {API}: {exc}")
        st.stop()

    if not data:
        st.info("No readings yet. Start the sensor emulator.")
        time.sleep(REFRESH)
        st.rerun()
        return

    df = pd.DataFrame(data)
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"])

    c1, c2, c3 = st.columns(3)
    latest = df.iloc[0]
    c1.metric("Moisture %", f"{latest['moisture_percent']:.1f}")
    c2.metric("Temp °C", f"{latest['temperature_c']:.1f}")
    c3.metric("pH", f"{latest['ph']:.2f}")

    st.subheader("Trends (most recent first)")
    chart_df = df.sort_values("created_at")
    st.line_chart(chart_df.set_index("created_at")[["moisture_percent", "temperature_c", "ph"]])

    st.subheader("Latest rows")
    st.dataframe(df.head(20), use_container_width=True)

    time.sleep(REFRESH)
    st.rerun()


if __name__ == "__main__":
    main()
