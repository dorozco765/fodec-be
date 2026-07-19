from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.associates import router as associates_router
from app.api.hello import router as hello_router

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://fodec-fe.web.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hola FastAPI"}

app.include_router(hello_router)
app.include_router(associates_router)
