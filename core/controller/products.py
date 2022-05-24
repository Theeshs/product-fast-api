from itertools import product
from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.models.products import (
    Currencies,
    Products
)
from core.routes import products
from core.schema.products import (
    Product,
    ProductCreateResponse
)

async def create_products(product: Product, db: Session) -> Optional[ProductCreateResponse]:
    """ 
        Creatign Products in the database and return
    """
    if product:
        product = product.dict()
        try:
            db_product = Products(**product)
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            currency_id = product.get("currency")
            currency = db.query(Currencies).filter(
                Currencies.id == currency_id
            ).first()
            if currency:
                db_product.currency_sign = currency.currency_sign
                db_product.currency_name = currency.currency_name
            return ProductCreateResponse.from_orm(db_product)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    else:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to process")


async def list_products(currency_id: int, db: Session) -> List[ProductCreateResponse]:
    """ 
        Listing all Products
    """
    try:
        products = []
        if currency_id:
            products = db.query(
                Products.id,
                Products.name,
                Products.price,
                Currencies.currency_sign,
                Currencies.currency_name
            ).outerjoin(
                Currencies
            ).filter(
                Products.currency == Currencies.id
            ).filter(
                Currencies.id == currency_id
            ).all()
        else:
            products = db.query(
                Products.id,
                Products.name,
                Products.price,
                Currencies.currency_sign,
                Currencies.currency_name
            ).outerjoin(
                Currencies
            ).filter(
                Products.currency == Currencies.id
            ).all()
        
        return products
            
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


async def list_products_by_id(id: int, currency_id: int, db: Session) -> Optional[ProductCreateResponse]:
    """ 
        Get Product by id
    """
    try:
        product = None
        if currency_id and id:
            product = db.query(
                Products.id,
                Products.name,
                Products.price,
                Currencies.currency_sign,
                Currencies.currency_name
            ).outerjoin(
                Currencies
            ).filter(
                Products.currency == Currencies.id
            ).filter(
                Currencies.id == currency_id
            ).filter(
                Products.id == id
            ).first()
        else:
            product = db.query(
                Products.id,
                Products.name,
                Products.price,
                Currencies.currency_sign,
                Currencies.currency_name
            ).outerjoin(
                Currencies
            ).filter(
                Products.id == id
            ).first()
        if not product:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        return ProductCreateResponse.from_orm(product)
            
    except Exception as e:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



async def update_product(
   id: int, update_request: Product, 
   db: Session,
    ) -> ProductCreateResponse:
    """ 
        updated Product by id
    """
    try:
        product = db.query(Products).filter(Products.id == id).first()
        if not product:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        product.name = update_request.name
        product.currency = update_request.currency
        product.price = update_request.price
        db.commit()
        db.refresh(product)
        return product
            
            
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def delelt_product(id: int, currency_id: int, db: Session) -> ProductCreateResponse:
    """ 
        Delete Product by id
    """
    try:
        product = None
        if id and currency_id:
            product = db.query(
                Products
            ).filter(
                Products.id == id,
                Products.currency == currency_id
            ).first()
        else:
            product = db.query(
                Products
            ).filter(
                Products.id == id
            ).first()

        if not product:
            return HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
            )
        db.delete(product)
        db.commit()
        return product
    except Exception as e:
        print(e)
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
