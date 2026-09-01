def test_insight_endpoint_returns_empty_list_when_no_telemetry(client):
  response = client.get(
    "/api/v1/insights"
  )

  assert response.status_code == 200
  assert response.json() == []


def test_insight_endpoint_generates_warning_for_low_soil_moisture(client):
  reading = {
    "device_id": "sensor-001",
    "field_id": "field-001",
    "metric": "soil_moisture",
    "value": 10.0,
    "unit": "percent",
    "timestamp": "2026-08-01T12:00:00Z",
  }

  create_response = client.post(
    "/api/v1/readings",
    json=reading,
  )

  assert create_response.status_code == 201

  response = client.get(
    "/api/v1/insights"
  )

  assert response.status_code == 200

  data = response.json()

  assert len(data) == 1
  assert data[0]["device_id"] == "sensor-001"
  assert data[0]["metric"] == "soil_moisture"
  assert data[0]["severity"] == "warning"
  assert "below" in data[0]["summary"].lower()
  assert "irrigation" in data[0]["recommendation"].lower()

def test_insight_endpoint_generates_normal_insight(client):
  reading = {
    "device_id": "sensor-001",
    "field_id": "field-001",
    "metric": "soil_moisture",
    "value": 50.0,
    "unit": "percent",
    "timestamp": "2026-09-01T12:00:00Z",
  }

  create_response = client.post(
    "/api/v1/readings",
    json=reading,
  )

  assert create_response.status_code == 201

  response = client.get(
    "/api/v1/insights"
  )

  assert response.status_code == 200

  data = response.json()

  assert len(data) == 1
  assert data[0]["severity"] == "normal"
  assert "expected range" in data[0]["summary"].lower()