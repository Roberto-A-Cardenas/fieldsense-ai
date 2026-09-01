from datetime import datetime, timezone

from app.db.models import TelemetryRecord
from app.services.anomaly import detect_anomaly


def make_reading(value: float) -> TelemetryRecord:
  return TelemetryRecord(
    device_id="sensor-001",
    field_id="field-001",
    metric="soil_moisture",
    value=value,
    unit="percent",
    timestamp=datetime(2026, 8, 31, 12, 0, tzinfo=timezone.utc),
  )

def test_normal_reading_is_not_anomalous():
  reading = make_reading(50.0)

  result = detect_anomaly(reading)

  assert result["classification"] == "NORMAL"
  assert result["status"] == "normal"
  assert result["threshold"] is None

def test_low_soil_moisture_is_detected():
  reading = make_reading(10.0)

  result = detect_anomaly(reading)

  assert result["classification"] == "LOW"
  assert result["status"] == "warning"
  assert result["threshold"] == 20.0

def test_high_soil_moisture_is_detected():
  reading = make_reading(95.0)

  result = detect_anomaly(reading)

  assert result["classification"] == "HIGH"
  assert result["status"] == "warning"
  assert result["threshold"] == 80.0

def test_anomaly_endpoint_return_only_anomalies(client):
    readings = [
        {
            "device_id": "sensor-001",
            "field_id": "field-001",
            "metric": "soil_moisture",
            "value": 10.0,
            "unit": "percent",
            "timestamp": "2026-08-31T10:00:00Z",
        },
        {
            "device_id": "sensor-001",
            "field_id": "field-001",
            "metric": "soil_moisture",
            "value": 50.0,
            "unit": "percent",
            "timestamp": "2026-08-31T11:00:00Z",
        },
        {
            "device_id": "sensor-001",
            "field_id": "field-001",
            "metric": "soil_moisture",
            "value": 95.0,
            "unit": "percent",
            "timestamp": "2026-08-31T12:00:00Z",
        },
    ]

    for reading in readings:
        response = client.post(
            "/api/v1/readings",
            json=reading,
        )
        assert response.status_code == 201

    response = client.get(
        "/api/v1/readings/anomalies"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    classifications = {
        item["classification"]
        for item in data
    }

    assert classifications == {"LOW", "HIGH"}


def test_anomaly_endpoint_filters_by_device_id(client):
    first_reading = {
        "device_id": "sensor-001",
        "field_id": "field-001",
        "metric": "soil_moisture",
        "value": 10.0,
        "unit": "percent",
        "timestamp": "2026-08-31T10:00:00Z",
    }

    second_reading = {
        "device_id": "sensor-002",
        "field_id": "field-001",
        "metric": "soil_moisture",
        "value": 95.0,
        "unit": "percent",
        "timestamp": "2026-08-31T11:00:00Z",
    }

    assert client.post(
        "/api/v1/readings",
        json=first_reading,
    ).status_code == 201

    assert client.post(
        "/api/v1/readings",
        json=second_reading,
    ).status_code == 201

    response = client.get(
        "/api/v1/readings/anomalies",
        params={"device_id": "sensor-001"},
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["device_id"] == "sensor-001"
    assert data[0]["classification"] == "LOW"


def test_anomaly_endpoint_filters_by_time_range(client):
    readings = [
        {
            "device_id": "sensor-001",
            "field_id": "field-001",
            "metric": "soil_moisture",
            "value": 10.0,
            "unit": "percent",
            "timestamp": "2026-08-31T08:00:00Z",
        },
        {
            "device_id": "sensor-001",
            "field_id": "field-001",
            "metric": "soil_moisture",
            "value": 95.0,
            "unit": "percent",
            "timestamp": "2026-08-31T12:00:00Z",
        },
    ]

    for reading in readings:
        assert client.post(
            "/api/v1/readings",
            json=reading,
        ).status_code == 201

    response = client.get(
        "/api/v1/readings/anomalies",
        params={
            "start_time": "2026-08-31T10:00:00Z",
            "end_time": "2026-08-31T14:00:00Z",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["value"] == 95.0
    assert data[0]["classification"] == "HIGH"


def test_anomaly_endpoint_rejects_invalid_time_range(client):
    response = client.get(
        "/api/v1/readings/anomalies",
        params={
            "start_time": "2026-08-31T14:00:00Z",
            "end_time": "2026-08-31T10:00:00Z",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "start_time must be before or equal to end_time"
    )


def test_anomaly_endpoint_filters_by_metric(client):
   soil_reading = {
      "device_id": "sensor-001",
      "field_id": "field-001",
      "metric": "soil_moisture",
      "value": 10.0,
      "unit": "percent",
      "timestamp": "2026-08-31T10:00:00Z",
   }

   temperature_reading = {
      "device_id": "sensor-001",
      "field_id": "field-001",
      "metric": "temperature",
      "value": 95.0,
      "unit": "celsius",
      "timestamp": "2026-08-31T11:00:00Z",
   }

   assert client.post(
      "/api/v1/readings",
      json=soil_reading,
   ).status_code == 201

   assert client.post(
      "/api/v1/readings",
      json=temperature_reading,
   ).status_code == 201

   response = client.get(
      "/api/v1/readings/anomalies",
      params={"metric": "soil_moisture"},
   )

   assert response.status_code == 200

   data = response.json()

   assert len(data) == 1
   assert data[0]["metric"] == "soil_moisture"
   assert data[0]["classification"] == "LOW"