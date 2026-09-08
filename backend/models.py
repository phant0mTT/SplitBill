from pydantic import BaseModel
from typing import List, Optional


class BillItem(BaseModel):
    name: str
    quantity: float
    price: float
    confidence: float = 1.0


class Bill(BaseModel):
    items: List[BillItem]
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    service_charge: Optional[float] = None
    discount: Optional[float] = None
    total: float


class SplitRequest(BaseModel):
    bill: Bill
    #people: List[str]
    assignments: dict[str, dict[str, float]]
    #assignments: dict[str, List[str]]