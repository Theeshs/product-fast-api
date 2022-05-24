from datetime import date
from locale import currency
from typing import List, Optional
from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: float
    currency: int


class ProductCreateResponse(BaseModel):
    id: int | None
    name: str | None
    price: float | None
    currency_sign: str | None
    currency_name: str | None

    class Config:
        orm_mode=True