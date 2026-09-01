from typing import Literal

from pydantic import BaseModel

InsightSeverity = Literal["normal", "warning", "critical"]

class InsightResponse(BaseModel):
  device_id: str
  metric: str
  summary: str
  recommendation: str
  severity: InsightSeverity