# app/core/config.py
from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    PROJECT_ROOT: str = str(Path(__file__).parent.parent.parent.parent)
    DATA_DIR: str = f"{PROJECT_ROOT}/data/processed"

    # Ollama local settings (không cần HF_TOKEN nữa)
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "mistral")  # hoặc qwen2.5:7b, llama3.1:8b,...

    # MongoDB local
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "nutrition_local")

    # Các giới hạn khác giữ nguyên
    MAX_ITEMS_PROMPT: int = 8
    MAX_TOKENS_PLAN: int = 2500
    MAX_TOKENS_NORMAL: int = 1200

    class Config:
        env_file = ".env"               # tự động load .env nếu có
        env_file_encoding = "utf-8"

settings = Settings()