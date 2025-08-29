from pydantic import BaseModel
from typing import List, Optional


class OfferSchema(BaseModel):
    url: Optional[str] = None
    original_url: Optional[str] = None
    title: Optional[str] = None
    shop: Optional[str] = None
    price: Optional[int] = None
    is_used: Optional[bool] = None

class ProductResponseSchema(BaseModel):
    url: str
    offers: List[OfferSchema]