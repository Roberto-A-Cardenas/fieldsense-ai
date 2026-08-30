# FieldSense API

FieldSense is a lightweight telemetry ingestion API built with FastAPI. It simulates the backend ingestion layer for distributed field sensors that send measurements such as soil moisture and other environmental telemetry.

The project demonstrates API design, request validation, relational persistence, automated testing, containerization, and continuous integration.

## Architecture

```text
Field Device / Sensor
        |
        v
POST /api/v1/readings
        |
        v
FastAPI
        |
        v
Pydantic Validation
        |
        v
SQLAlchemy
        |
        v
SQLite Database
        |
        v
GET /api/v1/readings
```

The application is packaged as a Docker container and validated automatically through GitHub Actions.

```text
Developer Push
      |
      v
GitHub Actions
      |
      +--> Install Dependencies
      |
      +--> Run Pytest
      |
      +--> Build Docker Image
```

## Technology Stack

* Python 3.14
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite
* Pytest
* Docker
* GitHub Actions

## Project Structure

```text
fieldsense-ai/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   ├── models/
│   │   └── telemetry.py
│   ├── routes/
│   │   └── telemetry.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   └── test_telemetry.py
├── Dockerfile
├── requirements.txt
└── README.md
```

## API Endpoints

### Create Telemetry Reading

`POST /api/v1/readings`

Example request:

```json
{
  "device_id": "sensor-001",
  "field_id": "field-alpha",
  "metric": "soil_moisture",
  "value": 34.7,
  "unit": "percent",
  "timestamp": "2026-08-29T18:00:00Z"
}
```

The API validates the payload, persists the telemetry record, and returns HTTP `201 Created`.

### List Telemetry Readings

`GET /api/v1/readings`

Returns persisted telemetry readings ordered by timestamp.

## Local Development

Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

The API is available at:

```text
http://localhost:8000
```

Interactive FastAPI documentation is available at:

```text
http://localhost:8000/docs
```

## Automated Tests

Run:

```bash
pytest -v
```

The test suite validates:

* successful telemetry ingestion
* invalid telemetry rejection
* database persistence
* telemetry retrieval through the GET endpoint

Tests use a dedicated SQLite test database and override FastAPI's database dependency so test execution does not modify development data.

The test database is recreated for each test, providing deterministic and isolated test execution.

## Docker

Build the container:

```bash
docker build -t fieldsense-ai:local .
```

Run it:

```bash
docker run --rm -p 8000:8000 fieldsense-ai:local
```

If port `8000` is already occupied:

```bash
docker run --rm -p 8001:8000 fieldsense-ai:local
```

Test the containerized API:

```bash
curl http://localhost:8001/api/v1/readings
```

## Continuous Integration

GitHub Actions runs automatically for pushes and pull requests targeting `main`.

The CI pipeline:

1. Checks out the repository.
2. Configures Python.
3. Installs project dependencies.
4. Runs the automated test suite.
5. Builds the Docker image.

This ensures application code is tested and container-buildable before changes progress further through the delivery lifecycle.

## Design Decisions

### FastAPI Dependency Injection

Database sessions are supplied through FastAPI's `Depends()` mechanism. Tests override the database dependency to redirect API operations to an isolated test database.

### Test Isolation

Development and test data are separated. Pytest fixtures recreate the test schema between tests, preventing repeated test runs from producing duplicate development records.

### Containerization

Docker packages the application and dependencies into a consistent runtime environment, reducing differences between developer, CI, and deployment environments.

### Continuous Integration

GitHub Actions validates every change automatically, providing rapid feedback when application tests or container builds fail.

## Current Scope

FieldSense currently represents the telemetry ingestion foundation of a larger cloud-native architecture. Future iterations could replace local SQLite persistence with managed cloud databases, introduce messaging or event-streaming services, add authentication, and integrate telemetry analytics and observability.
