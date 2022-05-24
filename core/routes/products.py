from msilib.schema import Error
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from db._db import get_db

from core.schema.products import (
    Product,
    ProductCreateResponse
)

from core.controller.products import (
    create_products,
    delelt_product,
    list_products,
    list_products_by_id,
    update_product
)

router = APIRouter()

@router.get(
    "/ping", tags=["ping"],
)
async def ping():
    return {"data": "pong"}

@router.post(
    "/products", tags=["products"],
    response_model=ProductCreateResponse, response_model_exclude_unset=True
)
async def product(product: Product, db: Session = Depends(get_db)):
    data = await create_products(product, db)
    return data


@router.get(
    "/products", tags=["products"],
    response_model=List[ProductCreateResponse], response_model_exclude_unset=True
)
async def product(currency: str | None = None, db: Session = Depends(get_db)):
    currency_id = None
    if currency:
        currency_id = int(currency)
    data = await list_products(currency_id, db)
    return data


@router.get(
    "/products/{id}", tags=["products"],
    response_model=Optional[ProductCreateResponse], response_model_exclude_unset=True
)
async def product(id: int, currency: str | None = None, db: Session = Depends(get_db)):
    currency_id = None
    if currency:
        currency_id = int(currency)
    data = await list_products_by_id(id, currency_id, db)
    return data


@router.put(
    "/products/{id}", tags=["products"],
    response_model=ProductCreateResponse, response_model_exclude_unset=True
)
async def product(
        product: Product, id: int, 
        db: Session = Depends(get_db)
    ):
    data = await update_product(id, product, db)
    return data


@router.delete(
    "/products/{id}", tags=["products"],
    response_model=ProductCreateResponse, response_model_exclude_unset=True
)
async def product(id: int, currency: str | None = None, db: Session = Depends(get_db)):
    currency_id = None
    if currency:
        currency_id = int(currency)
    data = await delelt_product(id, currency_id, db)
    return data