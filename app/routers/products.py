from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.database import get_session
from app.models import Product
from SalesAnalyticsAPI.app.productSchema import *

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

SessionDep = Annotated[Session, Depends(get_session)]

def get_product_or_404(product_id: int, session: Session) -> Product:
    statement = select(Product).where(Product.id == product_id)
    product = session.exec(statement).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=list[ProductRead], summary="Get all products", description="Retrieve all products available in the product catalog.")
def get_products(session: SessionDep, 
    offset: int = Query(default=0, ge=0, description="No. of items to skip"), 
    limit: int = Query(default=0, le=100, description="Max number of items to return")
):
    statement = select(Product).offset(offset).limit(limit)
    products = session.exec(statement).all()
    return products

@router.get("/{product_id}", response_model=ProductRead, summary="Get product by ID", description="Retrieve detailed information for a specific product using its database ID.")
def get_product(product_id: int, session: SessionDep):
    return get_product_or_404(product_id, session)

@router.post("/", response_model=ProductRead, status_code=201, summary="Create a new product", description="Create a new product in the database. Product IDs must be unique.")
def create_product(product: ProductCreate, session: SessionDep):

    existing_product = session.exec(
        select(Product).where(Product.product_id == product.product_id)
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=409,
            detail="A product with this product id already exists."
        )

    if product.sell_price > product.mrp:
        raise HTTPException(
            status_code=400,
            detail="Selling price cannot be greater than MRP."
        )

    discount = round(
        ((product.mrp-product.sell_price)/product.mrp) * 100
    )

    db_product = Product(
        **product.model_dump(),
        discount=discount
    )
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.put("/{product_id}", response_model=ProductRead, summary="Update a product", description="Update one or more fields of an existing product using its database ID." )
def update_product(product_id: int, product: ProductUpdate, session: SessionDep):
    statement = select(Product).where(Product.id == product_id)

    db_product = get_product_or_404(product_id, session)

    update_data = product.model_dump(exclude_unset=True)
    db_product.sqlmodel_update(update_data)

    if "sell_price" in update_data or "mrp" in update_data:
        if db_product.sell_price > db_product.mrp:
            raise HTTPException(
                status_code=400,
                detail="Selling Price cannot be greater than MRP"
            )
        db_product.discount = round(
            ((db_product.mrp-db_product.sell_price)/db_product.mrp) * 100
        )

    session.commit()
    session.refresh(db_product)

    return db_product

@router.delete("/{product_id}", summary="Delete a product", description="Delete a product from the database using its database ID.")
def delete_product(product_id: int, session: SessionDep):
    product = get_product_or_404(product_id, session)
    session.delete(product)
    session.commit()

    return {
        "message": "Product deleted successfully"
    }

