import psycopg2
from app.core.config import settings

def create_db():
    db_name = settings.POSTGRES_DB
    #host = settings.POSTGRES_SERVER
    port = settings.POSTGRES_PORT
    user = settings.POSTGRES_USER
    password = settings.POSTGRES_PASSWORD
    
    db_params = {
        "dbname": db_name,
        "host": "db", # This is the name of the service in the docker-compose.yml file
        "port": port,
        "user": user,
        "password": password
    }
    
    conn = psycopg2.connect(**db_params)
    
    conn.autocommit = True
    cursor = conn.cursor()
    
    try:
        # Check if the database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        if not exists:
            print(f"Database '{db_name}' does not exist, creating...")
            cursor.close()
            conn.close()
            
            # Create the database
            conn = psycopg2.connect(**db_params)
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"Database '{db_name}' created successfully")
        else:
            print(f"Database '{db_name}' already exists")
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()
        
if __name__ == "__main__":
    create_db()
        