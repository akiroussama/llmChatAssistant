import os

class Config:
  DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://llm_user:securepassword@postgres:5432/llm_chat_db")
  MODEL_HOST = os.getenv("MODEL_HOST", "ollama")
  MODEL_PORT = int(os.getenv("MODEL_PORT", 11434))