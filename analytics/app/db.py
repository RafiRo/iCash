import psycopg2
from app.config import DB_CONFIG

def get_db():
    return psycopg2.connect(**DB_CONFIG)
