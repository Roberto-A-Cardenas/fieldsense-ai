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