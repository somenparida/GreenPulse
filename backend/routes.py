from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database import SensorReading, get_db
from schemas import SensorReadingCreate, SensorReadingResponse
from datetime import datetime, timedelta
from sqlalchemy import desc

router = APIRouter(prefix="/api/v1", tags=["readings"])

@router.post("/telemetry", response_model=SensorReadingResponse)
def create_telemetry(reading: SensorReadingCreate, db: Session = Depends(get_db)):
    """Ingest telemetry from IoT devices"""
    db_reading = SensorReading(**reading.dict())
    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)
    return db_reading

@router.get("/readings", response_model=list[SensorReadingResponse])
def get_readings(
    limit: int = Query(100, ge=1, le=1000),
    plot_id: str = Query(None),
    db: Session = Depends(get_db)
):
    """Get recent sensor readings"""
    query = db.query(SensorReading)
    
    if plot_id:
        query = query.filter(SensorReading.plot_id == plot_id)
    
    readings = query.order_by(desc(SensorReading.timestamp)).limit(limit).all()
    return readings

@router.get("/readings/{reading_id}", response_model=SensorReadingResponse)
def get_reading(reading_id: int, db: Session = Depends(get_db)):
    """Get a specific reading by ID"""
    reading = db.query(SensorReading).filter(SensorReading.id == reading_id).first()
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    return reading

@router.get("/readings/plot/{plot_id}", response_model=list[SensorReadingResponse])
def get_plot_readings(
    plot_id: str,
    hours: int = Query(24, ge=1, le=720),
    db: Session = Depends(get_db)
):
    """Get readings for a specific plot in the last N hours"""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    readings = db.query(SensorReading).filter(
        (SensorReading.plot_id == plot_id) &
        (SensorReading.timestamp >= cutoff_time)
    ).order_by(SensorReading.timestamp).all()
    return readings

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get aggregated statistics"""
    readings = db.query(SensorReading).all()
    
    if not readings:
        return {
            "total_readings": 0,
            "unique_plots": 0,
            "avg_moisture": 0,
            "avg_temperature": 0,
            "avg_ph": 0
        }
    
    return {
        "total_readings": len(readings),
        "unique_plots": len(set(r.plot_id for r in readings)),
        "avg_moisture": sum(r.moisture for r in readings) / len(readings),
        "avg_temperature": sum(r.temperature for r in readings) / len(readings),
        "avg_ph": sum(r.ph for r in readings) / len(readings)
    }
