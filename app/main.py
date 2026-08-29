from fastapi import FastAPI

from app.db import models
from app.db.database import Base, engine
from app.routes.telemetry import router as telemetry_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(telemetry_router, prefix="/api/v1", tags=["telemetry"])

@app.get("/")
def root():
    return {"message": "FieldSense API is running"}
