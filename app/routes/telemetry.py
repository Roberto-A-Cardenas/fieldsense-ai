from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import TelemetryRecord
from app.models.telemetry import TelemetryReading

router = APIRouter()

@router.post("/readings", status_code=status.HTTP_201_CREATED)
def create_reading(reading: TelemetryReading, db: Session = Depends(get_db), ):
    record = TelemetryRecord(**reading.model_dump())

    db.add(record)
    db.commit()
    db.refresh(record)
    
    return {"message": "Telemetry reading received", "reading": reading}
