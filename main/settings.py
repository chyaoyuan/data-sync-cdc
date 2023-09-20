import os


class Settings:
    redis_broker = os.getenv('REDIS_BROKER', 'redis://localhost:6379/0')
    master_name = os.getenv("REDIS_SENTINEL_MASTER_NAME")
    pg_user = os.getenv('POSTGRES_USER', 'postgres')
    pg_password = os.getenv('POSTGRES_PASSWORD', 'postgres')
    pg_host = os.getenv('POSTGRES_HOST', 'localhost')
    pg_port = int(os.getenv('POSTGRES_PORT', '5432'))
    pg_database = os.getenv('POSTGRES_DB', 'data-sync')