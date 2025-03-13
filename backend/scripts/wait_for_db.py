import time
import psycopg2
from urllib.parse import urlparse
from app.core.config import settings

def wait_for_db():
    db_params = {
        "dbname": "postgres", # Default database name that always exists in postgres
        "host": "db", # This is the name of the service in the docker-compose.yml file
        "port": settings.POSTGRES_PORT,
        "user": settings.POSTGRES_USER,
        "password": settings.POSTGRES_PASSWORD
    }
    retries = 0
    while True:
        try:
            print(f"Attempting to connect to database at host={db_params['host']}, "
                  f"port={db_params['port']}, user={db_params['user']}, "
                  f"dbname={db_params['dbname']}")
            conn = psycopg2.connect(**db_params)
            conn.close()
            print("Database is ready")
            break
        except psycopg2.OperationalError as e:
            retries += 1
            print(f"Attempt: ({retries}), DB connection failed: {str(e)}")
            if retries >= 15:
                print("Database connection failed after max 15 retries")
                raise
            print(f"Waiting for database...")
            time.sleep(1)
            
if __name__ == "__main__":
    wait_for_db()
            
            