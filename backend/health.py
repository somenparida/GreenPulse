from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import HealthResponse
from datetime import datetime

router = APIRouter(tags=["health"])

@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    """Health check endpoint"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return HealthResponse(
        status="healthy",
        database=db_status,
        timestamp=datetime.utcnow()
    )

@router.get("/health/live")
def liveness_probe():
    """Kubernetes liveness probe"""
    return {"status": "alive"}

@router.get("/health/ready")
def readiness_probe(db: Session = Depends(get_db)):
    """Kubernetes readiness probe"""
    try:
        db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception:
        return {"status": "not_ready"}, 503
