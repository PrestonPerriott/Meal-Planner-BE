import sys
import logging
from backend.app.core.db import init_db
from backend.app.core.config import settings

print(f"Python path: {sys.executable}")
print(f"Python version: {sys.version}")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init() -> None:
     init_db()

def main() -> None:
    logger.info("Creating initial data")
    logger.info(f"Using database: {settings.SQLALCHEMY_DATABASE_URL}")
    init()
    logger.info("Initial data created")

if __name__ == "__main__":
    main()