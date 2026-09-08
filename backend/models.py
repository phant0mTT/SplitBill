from pydantic import BaseModel,Field
from typing import List, Optional


class BillItem(BaseModel):
    name: str
    quantity: float = Field(gt=0)
    price: float = Field(ge=0)
    confidence: float = Field(ge=0, le=1)


class Bill(BaseModel):
    items: List[BillItem]

    subtotal: float = Field(ge=0)
    tax: float = Field(ge=0)
    service_charge: float = Field(ge=0)
    discount: float = Field(ge=0)

    total: float = Field(ge=0)


class SplitRequest(BaseModel):
    bill: Bill
    #people: List[str]
    assignments: dict[str, dict[str, float]]
    #assignments: dict[str, List[str]]