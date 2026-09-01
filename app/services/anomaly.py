from app.db.models import TelemetryRecord


THRESHOLDS = {
  "soil_moisture": {
    "low": 20.0,
    "high": 80.0,
  },
}

def detect_anomaly(reading: TelemetryRecord) -> dict:
  thresholds = THRESHOLDS.get(reading.metric)

  if thresholds is None:
    return {
      "device_id": reading.device_id,
      "metric": reading.metric,
      "value": reading.value,
      "threshold": None,
      "classification": "NORMAL",
      "status": "normal",
      "timestamp": reading.timestamp,
    }

  if reading.value < thresholds["low"]:
    return {
      "device_id": reading.device_id,
      "metric": reading.metric,
      "value": reading.value,
      "threshold": thresholds["low"],
      "classification": "LOW",
      "status": "warning",
      "timestamp": reading.timestamp,
    }

  if reading.value > thresholds["high"]:
      return {
        "device_id": reading.device_id,
        "metric": reading.metric,
        "value": reading.value,
        "threshold": thresholds["high"],
        "classification": "HIGH",
        "status": "warning",
        "timestamp": reading.timestamp,
      }

  return{
    "device_id": reading.device_id,
    "metric": reading.metric,
    "value": reading.value,
    "threshold": None,
    "classification": "NORMAL",
    "status": "normal",
    "timestamp": reading.timestamp,
  }