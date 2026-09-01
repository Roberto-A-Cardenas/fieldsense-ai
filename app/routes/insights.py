from  fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import TelemetryRecord
from app.models.insight import InsightResponse
from app.services.insights import InsightService


router = APIRouter()


@router.get(
  "/insights",
  response_model=list[InsightResponse],
)
def get_insights(
  device_id: str | None = None,
  metric: str | None = None,
  db: Session = Depends(get_db),
):

  statement = select(TelemetryRecord)

  if device_id is not None:
    statement = statement.where(
      TelemetryRecord.device_id == device_id
    )

  if metric is not None:
    statement = statement.where(
      TelemetryRecord.metric == metric
    )

  statement = statement.order_by(
    TelemetryRecord.timestamp.desc()
  )

  records = db.scalars(statement).all()

  service = InsightService()

  return [
    service.generate_from_reading(record)
    for record in records
  ]