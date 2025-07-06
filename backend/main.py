# Entry point for FastAPI app
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def root():
    return {"message": "MindMate Backend Running"}