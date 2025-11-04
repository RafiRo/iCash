import os

def read_secret_or_env(name: str) -> str:
    """Read from ENV or Docker Secret file."""
    value = os.getenv(name)
    if value:
        return value.strip()

    file_path = os.getenv(f"{name}_FILE")
    if file_path and os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read().strip()

    raise RuntimeError(f"Missing required secret: {name}")


DB_CONFIG = {
    "dbname": read_secret_or_env("POSTGRES_DB"),
    "user": read_secret_or_env("POSTGRES_USER"),
    "password": read_secret_or_env("POSTGRES_PASSWORD"),
    "host": read_secret_or_env("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
}

APP_TITLE = os.getenv("APP_TITLE", "Analytics API")
APP_VERSION = os.getenv("APP_VERSION", "1.0")
