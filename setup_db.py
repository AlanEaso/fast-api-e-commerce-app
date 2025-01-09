# setup_db.py
import psycopg
from app.core.config import settings

async def create_database():
    # Connection string for the default postgres database
    conninfo = f"dbname=postgres user={settings.POSTGRES_USER} password={settings.POSTGRES_PASSWORD} host={settings.POSTGRES_SERVER} port={settings.DB_PORT}"
    
    try:
        # Connect to default postgres database
        async with await psycopg.AsyncConnection.connect(conninfo) as conn:
            async with conn.cursor() as cur:
                # Set autocommit to create database
                await conn.set_autocommit(True)
                
                # Check if database exists
                await cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s", (settings.POSTGRES_DB,))
                exists = await cur.fetchone()
                
                if not exists:
                    try:
                        # Escape the database name to handle special characters
                        await cur.execute(f'CREATE DATABASE "{settings.POSTGRES_DB}"')
                        print(f"Database {settings.POSTGRES_DB} created successfully!")
                    except Exception as e:
                        print(f"Error creating database: {e}")
                else:
                    print(f"Database {settings.POSTGRES_DB} already exists.")
    
    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_database())