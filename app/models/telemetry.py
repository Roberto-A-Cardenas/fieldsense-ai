from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TelemetryReading(BaseModel):
 device_id: str
 field_id: str
 metric: str
 value: float
 unit: str
 timestamp: datetime

class TelemetryAnalyticsResponse(BaseModel):
 count: int
 average: float | None
 minimum: float | None
 maximum: float | None

class TelemetryRecordResponse(TelemetryReading):
 id: int
 created_at: datetime

 model_config = ConfigDict(from_attributes=True)

class TelemetryAnomalyResponse(BaseModel):
 device_id: str
 metric: str
 value: float
 threshold: float | None
 classification: str
 status: str
 timestamp: datetime