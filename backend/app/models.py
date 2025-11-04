from pydantic import BaseModel

class PurchaseRequest(BaseModel):
    supermarket_id: str
    user_id: str | None = None
    items: list[int]