from datetime import datetime

from pydantic import BaseModel

class TelemetryReading(BaseModel):
	device_id: str
	field_id: str
	metric: str
	value: float
	unit: str
	timestamp: datetime
