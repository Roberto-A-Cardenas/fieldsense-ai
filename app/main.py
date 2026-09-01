from fastapi import FastAPI

from app.db import models
from app.db.database import Base, engine
from app.routes.telemetry import router as telemetry_router
from app.routes.insights import router as insights_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(telemetry_router, prefix="/api/v1", tags=["telemetry"])

app.include_router(
    insights_router,
    prefix="/api/v1",
    tags=["insights"],
)

@app.get("/")
def root():
    return {"message": "FieldSense API is running"}
