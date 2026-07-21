import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Rosenix AI OS"
    VERSION: str = "2.0.0"
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    SECRET_KEY: str = "rosenix-cyber-secret-key-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    UPLOAD_DIR: str = os.path.join(BASE_DIR, "uploads")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
