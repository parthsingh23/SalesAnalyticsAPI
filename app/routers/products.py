from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlalchemy import func

from app.database import get_session
from app.models import Sale
from app.schemas import TopProductResponse

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.get("/top", response_model=list[TopProductResponse])
def get_top_products(limit: int = 10, session: Session = Depends(get_session)):
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