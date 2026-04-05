import random

from telemetry_logic import sample_telemetry


def test_sample_telemetry_deterministic():
    rng = random.Random(42)
    row = sample_telemetry("plot-x", rng=rng)
    assert row["plot_id"] == "plot-x"
    assert 18.0 <= row["moisture_percent"] <= 65.0
    assert 12.0 <= row["temperature_c"] <= 38.0
    assert 5.5 <= row["ph"] <= 8.2
