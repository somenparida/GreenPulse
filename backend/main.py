from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import router as readings_router
from health import router as health_router
from config import settings

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(readings_router)
app.include_router(health_router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {
        "name": "GreenPulse API",
        "version": settings.api_version,
        "docs": "/docs",
        "endpoints": {
            "readings": "/api/v1/readings",
            "telemetry": "/api/v1/telemetry",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
