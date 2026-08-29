from fastapi import FastAPI

from app.routes.telemetry import router as telemetry_router

app = FastAPI()

app.include_router(telemetry_router, prefix="/api/v1", tags=["telemetry"])

@app.get("/")
def root():
    return {"message": "FieldSense API is running"}
