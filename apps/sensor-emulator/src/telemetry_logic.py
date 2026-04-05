"""Pure functions for telemetry generation (testable without I/O)."""
from __future__ import annotations

import random
from typing import Any, Dict


def sample_telemetry(plot_id: str, rng: random.Random | None = None) -> Dict[str, Any]:
    r = rng or random
    return {
        "plot_id": plot_id,
        "moisture_percent": round(r.uniform(18.0, 65.0), 2),
        "temperature_c": round(r.uniform(12.0, 38.0), 2),
        "ph": round(r.uniform(5.5, 8.2), 2),
    }
