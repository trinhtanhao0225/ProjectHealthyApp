from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.v1.router import api_router
from backend.core.config import settings
from backend.core.database import init_db   # ← import ở đây

app = FastAPI(
    title="Nutrition RAG Local API",
    description="API dinh dưỡng dùng Ollama + MongoDB local",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_db()

# =========================

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Nutrition Local API is running"}