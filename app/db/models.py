from datetime import datetime

from sqlalchemy import DateTime, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class TelemetryRecord(Base):
  __tablename__ = "telemetry_readings"

  id: Mapped[int] = mapped_column(primary_key=True)

  device_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True, )

  field_id: Mapped[str] = mapped_column(String(100), nullable=False, index=True, )

  metric: Mapped[str] = mapped_column(String(50), nullable=False, )

  value: Mapped[float] = mapped_column(Float, nullable=False, )

  unit: Mapped[str] = mapped_column(String(50), nullable=False, )

  timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, )

  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False, )

  