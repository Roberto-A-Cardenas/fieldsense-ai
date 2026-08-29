from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FieldSense API is running"}
