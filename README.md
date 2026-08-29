# FieldSense API

## Purpose

    FieldSense API is a lightweight telemetry ingestion service designed to receive measurements from distributed field devices. This lab establishes the application boundary for a cloud-native ingestion layer that can later integrate with messaging, persistence and analytics services.

## Project structure

app/
Application source code, including API routes, request/response models, configuration and application startup.
tests/
Automated tests used to validate application behavior independently of the runtime environment.

## Setup

    The project uses a Python virtual environment to isolate application dependencies from the host system. Runtime and test dependencies are declared in requirements.txt so the development environment can be recreated consistently across developer machines, CI pipelines and container builds.
