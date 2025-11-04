from app.models import PurchaseRequest
from fastapi import APIRouter, HTTPException
import uuid
from datetime import datetime, timezone
from app.lifespan import products_cache, supermarkets_cache, users_cache
from app.db import get_db




router = APIRouter()

@router.get("/init")
def get_init_data():
    return {
        "products": products_cache,
        "supermarkets": supermarkets_cache,
        "users": users_cache,
    }

@router.post("/add_item")
def add_item(purchase: PurchaseRequest):
    conn = get_db()
    cur = conn.cursor()

    user_id = purchase.user_id or str(uuid.uuid4())

    # Check if user exists; if not, create
    cur.execute("SELECT 1 FROM app_user WHERE user_id = %s;", (user_id,))
    if not cur.fetchone():
        cur.execute("INSERT INTO app_user (user_id) VALUES (%s);", (user_id,))

    # Validate products and calculate total
    price_lookup = {p["id"]: p["price"] for p in products_cache}
    name_lookup = {p["id"]: p["name"] for p in products_cache}

    total = 0.0
    item_names = []

    for pid in purchase.items:
        if pid not in price_lookup:
            raise HTTPException(status_code=400, detail=f"Unknown product ID {pid}")
        total += price_lookup[pid]
        item_names.append(name_lookup[pid])

    item_list = ", ".join(item_names)

    # Insert purchase
    cur.execute("""
        INSERT INTO purchases (supermarket_id, timestamp, user_id, item_list, total_amount)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, timestamp;
    """, (
        purchase.supermarket_id,
        datetime.now(timezone.utc),
        user_id,
        item_list,
        total
    ))

    purchase_id, timestamp = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return {
        "purchase_id": purchase_id,
        "user_id": user_id,
        "items": item_names,
        "total_amount": total,
        "timestamp": timestamp.isoformat(),
    }

@router.get("/health")
def health():
    """Healthcheck endpoint."""
    try:
        conn = get_db()
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
