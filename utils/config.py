from pydantic import BaseSettings, Field
from typing import Optional
from pathlib import Path
from os import environ
import logging

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    HOST: str = Field("0.0.0.0", env="HOST")
    PORT: int = Field(8000, env="PORT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"
    LOG_DIR: Optional[str] = Field(Path(__file__).parent.absolute() / "logs")
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{settings.LOG_DIR}/library_backend.log"),
        logging.StreamHandler(),
    ],
)

# Define a function to log debug messages
def debug(message: str):
    logging.debug(message)

# Define a function to log info messages
def info(message: str):
    logging.info(message)

# Define a function to log warning messages
def warning(message: str):
    logging.warning(message)

# Define a function to log error messages
def error(message: str, exc_info=True):
    logging.error(message, exc_info=exc_info)

# Define a function to log critical messages
def critical(message: str):
    logging.critical(message)