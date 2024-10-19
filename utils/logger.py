import logging
from .config import settings

# Initialize a logger for this file
logger = logging.getLogger(__name__)

# Configure the logger to write to a file and to the console
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
    logger.debug(message)

# Define a function to log info messages
def info(message: str):
    logger.info(message)

# Define a function to log warning messages
def warning(message: str):
    logger.warning(message)

# Define a function to log error messages
def error(message: str, exc_info=True):
    logger.error(message, exc_info=exc_info)

# Define a function to log critical messages
def critical(message: str):
    logger.critical(message)