from fastapi import FastAPI
from app.routes import router
from app.lifespan import lifespan
from app.config import APP_TITLE, APP_VERSION
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=APP_TITLE, version=APP_VERSION, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
