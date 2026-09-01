from datetime import datetime, timezone

from app.db.models import TelemetryRecord
from app.services.insights import InsightService

def test_generate_low_soil_moisture_insight():
  service = InsightService()

  anomaly = {
    "device_id": "sensor-001",
    "metric": "soil_moisture",
    "value": 10.0,
    "threshold": 20.0,
    "classification": "LOW",
    "status": "warning",
    "timestamp": None,
  }

  result = service.generate_from_anomaly(anomaly)

  assert result.device_id == "sensor-001"
  assert result.metric == "soil_moisture"
  assert result.severity == "warning"
  assert "below" in result.summary.lower()
  assert "irrigation" in result.recommendation.lower()

def test_generate_high_soil_moisture_insight():
  service = InsightService()

  anomaly = {
    "device_id": "sensor-001",
    "metric": "soil_moisture",
    "value": 90.0,
    "threshold": 80.0,
    "classification": "HIGH",
    "status": "warning",
    "timestamp": None,
  }

  result = service.generate_from_anomaly(anomaly)

  assert result.device_id == "sensor-001"
  assert result.metric == "soil_moisture"
  assert result.severity == "warning"
  assert "above" in result.summary.lower()
  assert "drainage" in result.recommendation.lower()

def test_generate_normal_insight():
  service = InsightService()

  anomaly = {
    "device_id": "sensor-001",
    "metric": "soil_moisture",
    "value": 50.0,
    "threshold": None,
    "classification": "NORMAL",
    "status": "normal",
    "timestamp": None,
  }

  result = service.generate_from_anomaly(anomaly)

  assert result.device_id == "sensor-001"
  assert result.metric == "soil_moisture"
  assert result.severity == "normal"
  assert "expected range" in result.summary.lower()
  assert "monitoring" in result.recommendation.lower()

def test_generate_insight_from_real_telemetry_reading():
  service = InsightService()

  reading = TelemetryRecord(
    device_id="sensor-001",
    field_id="field-001",
    metric="soil_moisture",
    value=10.0,
    unit="percent",
    timestamp=datetime(
      2026,
      9,
      1,
      12,
      0,
      tzinfo=timezone.utc,
    ),
  )

  result = service.generate_from_reading(reading)

  assert result.device_id == "sensor-001"
  assert result.metric == "soil_moisture"
  assert result.severity == "warning"
  assert "below" in result.summary.lower()
  assert "irrigation" in result.recommendation.lower()