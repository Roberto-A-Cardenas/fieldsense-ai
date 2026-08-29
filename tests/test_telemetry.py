from fastapi.testclient import TestClient 

from app.main import app

client = TestClient(app)

def test_create_telemetry_reading():
  Payload = {"device_id": "sensor-001", "field_id": "field-alpha", "metric": "soil_moisture",
             "value": 34.7, "unit": "percent", "timestamp": "2026-08-28T21:45:00z", }
  response = client.post("/api/v1/readings", json=Payload)

  assert response.status_code == 201
  assert response.json()["reading"]["device_id"] == "sensor-001"
  assert response.json()["reading"]["value"] == 34.7


def test_reject_invalid_telemetry_value():
  payload = {"device_id": "sensor-001", "field_id": "field-alpha", "metric": "soil_moisture", "value": "not-a-number", "unit": "percent", "timestamp": "206-08-28T21:45:00Z", }

  response = client.post("/api/v1/readings", json=payload)

  assert response.status_code == 422