from fastapi import FastAPI
from app.api.hello import router as hello_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hola FastAPI"}

app.include_router(hello_router)
