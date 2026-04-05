from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SensorReadingCreate(BaseModel):
    plot_id: str
    moisture: float
    temperature: float
    ph: float

class SensorReadingResponse(SensorReadingCreate):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True

class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: datetime
