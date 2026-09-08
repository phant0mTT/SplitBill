from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class BillItem(BaseModel):
    id: Optional[int] = None

    name: str

    quantity: float = Field(
        ge=0,
        description="Quantity printed on the bill."
    )

    price: float = Field(
        ge=0,
        description="Pre-tax price for this line item."
    )

    confidence: float = Field(
        ge=0,
        le=1,
        description="Confidence that the extracted item information is correct."
    )


class Bill(BaseModel):
    items: List[BillItem]

    subtotal: float = Field(ge=0)
    tax: float = Field(ge=0)
    service_charge: float = Field(ge=0)
    discount: float = Field(ge=0)
    total: float = Field(ge=0)


class SplitRequest(BaseModel):
    bill: Bill
    assignments: Dict[int, Dict[str, float]]