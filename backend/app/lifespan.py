import time
import psycopg2
from contextlib import asynccontextmanager
from app.db import get_db

products_cache = []
supermarkets_cache = []
users_cache = []

@asynccontextmanager
async def lifespan(app):
    print("Starting FastAPI app...")
    #Load all items to memory (cache),  in the future can be replaced with Redis
    for attempt in range(10):
        try:
            conn = get_db()
            cur = conn.cursor()

            cur.execute("SELECT id, product_name, unit_price FROM products_list ORDER BY id;")
            rows = cur.fetchall()
            products_cache.extend(
                {"id": r[0], "name": r[1], "price": float(r[2])} for r in rows
            )
            # Supermarkets
            cur.execute("SELECT supermarket_id FROM supermarket ORDER BY supermarket_id;")
            supermarkets_cache.extend(r[0] for r in cur.fetchall())

            # Users
            cur.execute("SELECT user_id FROM app_user ORDER BY id;")
            users_cache.extend(r[0] for r in cur.fetchall())

            cur.close()
            conn.close()
            break

        except psycopg2.OperationalError as e:
            #retry db connection (10 times)
            time.sleep(3)
    else:
        print("Could not connect to database after 10 attempts.")

    yield
    print("App shutting down.")
