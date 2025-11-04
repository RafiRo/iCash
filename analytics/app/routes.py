from fastapi import APIRouter
from app.db import get_db

router = APIRouter()

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{supermarket_id}")
def supermarket_statistics(supermarket_id: str):
    try:
        conn = get_db()
        cur = conn.cursor()

        # Ensure supermarket exists
        cur.execute("SELECT 1 FROM supermarket WHERE supermarket_id = %s;", (supermarket_id,))
        if not cur.fetchone():
            raise HTTPException(status_code=404, detail="Supermarket not found")

        # Unique buyers
        cur.execute("""
             SELECT COUNT(DISTINCT user_id)
             FROM purchases
             WHERE supermarket_id = %s;
         """, (supermarket_id,))
        unique_buyers = cur.fetchone()[0] or 0

        # Special users
        cur.execute("""
            SELECT user_id, COUNT(*) AS purchase_count
            FROM purchases
            WHERE supermarket_id = %s
            GROUP BY user_id
            HAVING COUNT(*) > 2
            ORDER BY purchase_count DESC, user_id;
        """, (supermarket_id,))
        rows = cur.fetchall()

        special_users = [{"user_id": r[0], "purchase_count": r[1]} for r in rows]

        # Top items
        cur.execute("""
                WITH ranked_items AS (
                  SELECT 
                    TRIM(item) AS item_name,
                    COUNT(*) AS frequency,
                    DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS rnk
                  FROM (
                    SELECT unnest(string_to_array(item_list, ',')) AS item
                    FROM purchases
                    WHERE supermarket_id = %s
                  ) AS t
                  GROUP BY TRIM(item)
                )
                SELECT item_name, frequency
                FROM ranked_items
                WHERE rnk <= 3
                ORDER BY frequency DESC, item_name;
        """, (supermarket_id,))

        top_items = [{"item_name": row[0], "count": row[1]} for row in cur.fetchall()]

        cur.close()
        conn.close()

        return {
            "unique_buyers": unique_buyers,
            "special_users": special_users,
            "top_items": top_items
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error in analytics: {e}")
        raise HTTPException(status_code=500, detail="Analytics computation failed")


@router.get("/health")
def health():
    """Healthcheck endpoint."""
    try:
        conn = get_db()
        conn.close()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "details": str(e)}
