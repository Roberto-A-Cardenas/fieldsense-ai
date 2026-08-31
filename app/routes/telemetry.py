from datetime import datetime

from fastapi import APIRouter, Depends, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import TelemetryRecord
from app.models.telemetry import TelemetryReading, TelemetryRecordResponse


router = APIRouter()


@router.post("/readings", status_code=status.HTTP_201_CREATED)
def create_reading(
    reading: TelemetryReading,
    db: Session = Depends(get_db),
    ):
    record = TelemetryRecord(**reading.model_dump())

    db.add(record)
    db.commit()
    db.refresh(record)
    
    return {"message": "Telemetry reading received", "reading": reading}

@router.get(
        "/readings",
        response_model=list[TelemetryRecordResponse],
)

def list_readings(
    device_id: str | None = None,
    db: Session = Depends(get_db),
):

    statement = select(TelemetryRecord)

    if device_id is not None:
        statement = statement.where(
            TelemetryRecord.device_id == device_id
        )

    statement = statement.order_by(
        TelemetryRecord.timestamp.desc()
    )

    records = db.scalars(statement).all()

    return records

@router.get("/readings/analytics")
def get_reading_analytics(
    device_id: str,
    start_time: datetime | None = None,
    end_time: datetime | None = None,
    db: Session = Depends(get_db),
):
    statement = select(
        func.count(TelemetryRecord.value),
        func.avg(TelemetryRecord.value),
        func.min(TelemetryRecord.value),
        func.max(TelemetryRecord.value),
    ).where(
        TelemetryRecord.device_id == device_id
    )

    if start_time is not None:
        statement = statement.where(
            TelemetryRecord.timestamp <= end_time
        )

    count, average, minimum, maximum = db.execute(statement).one()

    return {
        "count": count,
        "average": average,
        "minimum": minimum,
        "maximum": maximum,
    }
