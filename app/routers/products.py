from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlmodel import Session, select

from app.database import get_session
from app.models import Product, Sale
from app.schemas import (
    ProductCreate,
    ProductRead,
    ProductUpdate,
    TopProductResponse,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/", response_model=list[ProductRead], description="Display all products")
def get_products(session: SessionDep):
    statement = select(Product)
    products = session.exec(statement).all()
    return products

@router.get("/top", response_model=list[TopProductResponse])
def get_top_products(limit: int = 10, session: SessionDep = None):
    query = (
        select(
            Sale.sku,
            Sale.brand,
            func.sum(Sale.units_sold)
        ).group_by(Sale.sku, Sale.brand).order_by(func.sum(Sale.units_sold).desc()).limit(limit)
    )

    results = session.exec(query).all()

    return [
        TopProductResponse(
            sku = row[0],
            brand = row[1],
            units_sold= row[2]
        )
        for row in results
    ]

@router.get("/{product_id}", response_model=ProductRead, description="Display single product by id")
def get_product(product_id: int, session: SessionDep):
    statement = select(Product).where(Product.id == product_id)
    product = session.exec(statement).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product

@router.post("/", response_model=ProductRead, status_code=201, summary="Creates a new product in the database.")
def create_product(product: ProductCreate, session: SessionDep):

    existing_product = session.exec(
        select(Product).where(Product.product_id == product.product_id)
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=409,
            detail="Product Already Exists"
        )

    db_product = Product.model_validate(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=ProductRead)
def update_product(product_id: int, product: ProductUpdate, session: SessionDep):
    statement = select(Product).where(Product.id == product_id)

    db_product = session.exec(statement).first()

    if db_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    db_product.sqlmodel_update(
        product.model_dump(exclude_unset=True)
    )  

    session.commit()
    session.refresh(db_product)

    return db_product

@router.delete("/{product_id}")
def delete_product(product_id: int, session: SessionDep):
    statement = select(Product).where(Product.id == product_id)

    product = session.exec(statement).first()
    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    session.delete(product)
    session.commit()

    return {
        "message": "Product deleted successfully"
    }

