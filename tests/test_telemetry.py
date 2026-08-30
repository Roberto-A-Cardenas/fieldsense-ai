from fastapi.testclient import TestClient 
from sqlalchemy import select

from app.db.models import TelemetryRecord

from app.main import app

client = TestClient(app)

def test_create_telemetry_reading():
  Payload = {"device_id": "sensor-001", 
             "field_id": "field-alpha", 
             "metric": "soil_moisture",
             "value": 34.7, 
             "unit": "percent", 
             "timestamp": "2026-08-28T21:45:00z", 
  }
  
  response = client.post("/api/v1/readings", json=Payload)

  assert response.status_code == 201
  assert response.json()["reading"]["device_id"] == "sensor-001"
  assert response.json()["reading"]["value"] == 34.7


def test_reject_invalid_telemetry_value():
  payload = {"device_id": "sensor-001", 
             "field_id": "field-alpha", 
             "metric": "soil_moisture", 
             "value": "not-a-number", 
             "unit": "percent", 
             "timestamp": "206-08-28T21:45:00Z", 
  }

  response = client.post("/api/v1/readings", json=payload)

  assert response.status_code == 422


def test_telemetry_reading_is_persisted(db_session):
  payload = {"device_id": "sensor-persist-001", 
             "field_id": "field-test", 
             "metric": "soil_moisture", 
             "value": 42.5, 
             "unit": "percent", 
             "timestamp": "2026-08-29T18:00:00Z", 
  }

  response = client.post("/api/v1/readings", json=payload)

  assert response.status_code == 201

  record = db_session.scalar(
    select(TelemetryRecord).where(
      TelemetryRecord.device_id == "sensor-persist-001"
    )
)

  assert record is not None
  assert record.field_id == "field-test"
  assert record.metric == "soil_moisture"
  assert record.value == 42.5
  assert record.unit == "percent"


def test_list_telemetry_readings():
  payload = {"device_id": "sensor-list-001", 
             "field_id": "field_list", 
             "metric": "soil_moisture", 
             "value": 55.2, 
             "unit": "percent", 
             "timestamp": "2026-08-29T19:00:00Z",
   }

  create_response = client.post("/api/v1/readings", json=payload)

  assert create_response.status_code == 201

  response = client.get("/api/v1/readings")

  assert response.status_code == 200

  readings = response.json()

  assert isinstance(readings, list)
  assert any(
    reading["device_id"] == "sensor-list-001"
    for reading in readings
)


def test_filter_telemetry_by_device_id():
  first_payload = {
    "device_id": "sensor-filter-001",
    "field_id": "field-alpha",
    "metric": "soil_moisture",
    "value": 31.5,
    "unit": "percent",
    "timestamp": "2026-08-30T15:00:00Z",
  }

  second_payload = {
    "device_id": "sensor-filter-002",
    "field_id": "field-alpha",
    "metric": "soil_moisture",
    "value": 47.8,
    "unit": "percent",
    "timestamp": "2026-08-30T15:05:00Z",
  }

  first_response = client.post("/api/v1/readings", json=first_payload)
  second_response = client.post("/api/v1/readings", json=second_payload)

  assert first_response.status_code == 201
  assert second_response.status_code == 201

  response = client.get(
    "/api/v1/readings",
    params={"device_id": "sensor-filter-001"},
  )

  assert response.status_code == 200

  readings = response.json()

  assert len(readings) >= 1
  assert any(
    reading["device_id"] == "sensor-filter-001"
    for reading in readings
  )
  assert all(
    reading["device_id"] == "sensor-filter-001"
    for reading in readings
  )
  