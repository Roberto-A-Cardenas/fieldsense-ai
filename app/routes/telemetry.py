from fastapi import APIRouter, status

from app.models.telemetry import TelemetryReading

router = APIRouter()

@router.post("/readings", status_code=status.HTTP_201_CREATED)
def create_reading(reading: TelemetryReading):
    return {"message": "Telemetry reading received", "reading": reading}
