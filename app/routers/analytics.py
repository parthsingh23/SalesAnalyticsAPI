from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy import func, text

from app.database import get_session
from app.models import Sale
from app.schemas import KPIResponses, SalesTrendResponse, SalesByRegionResponses, SalesByCategory, Granularity

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/kpis", response_model=KPIResponses, summary="Get business KPIs", description="Retrieve key performance indicators including total records, units sold, revenue, average price, delivered quantity, and unique products.")
def get_kpis(session: Session = Depends(get_session)):
    query = select(
        func.count(Sale.id),
        func.sum(Sale.units_sold),
        func.sum(Sale.delivered_qty),
        func.sum(Sale.price_unit * Sale.units_sold),
        func.avg(Sale.price_unit),
        func.count(func.distinct(Sale.sku))
    )

    result = session.exec(query).one()

    return KPIResponses(
        total_records=result[0],
        total_units_sold=result[1],
        total_delivered_qty=result[2],
        total_revenue=round(result[3], 2),
        average_price=round(result[4], 2),
        unique_products=result[5]
    )


@router.get("/sales/trend", response_model=list[SalesTrendResponse], summary="Get sales trend", description="Get sales trends grouped by daily, weekly, monthly, or yearly intervals using the 'granularity' query parameter.")
def get_sales_trend(session: Session = Depends(get_session), granularity: Granularity = Granularity.daily):
    period_map = {
        Granularity.daily: text("'daily'"),
        Granularity.weekly: text("'week'"),
        Granularity.monthly: text("'month'"),
        Granularity.yearly: text("'year'")
    }

    period = period_map[granularity]

    query = (
        select(
            func.date_trunc(period, Sale.date).label("period"),
            func.sum(Sale.units_sold)
        ).group_by("period").order_by("period")
    )
    results = session.exec(query).all()

    return [
        SalesTrendResponse(
            date=row[0].date(),
            units_sold=row[1]
        )
        for row in results
    ]


@router.get("/sales/by-region", response_model=list[SalesByRegionResponses], summary="Get sales by region", description="Get total units sold grouped by region.")
def get_sales_by_region(session: Session = Depends(get_session)):
    query = (
        select(
            Sale.region,
            func.sum(Sale.units_sold)
        ).group_by(Sale.region).order_by(func.sum(Sale.units_sold).desc())
    )

    results = session.exec(query).all()

    return [
        SalesByRegionResponses(
            region=row[0],
            units_sold=row[1]
        )
        for row in results
    ]

@router.get("/sales/by-category", response_model=list[SalesByCategory], summary="Get sales by category", description="Get total units sold grouped by product category")
def get_sales_by_category(session: Session = Depends(get_session)):
    query = (
        select(
            Sale.category,
            func.sum(Sale.units_sold)
        ).group_by(Sale.category).order_by(func.sum(Sale.units_sold).desc())
    )

    results = session.exec(query).all()

    return [
        SalesByCategory(
            category=row[0],
            units_sold=row[1]
        )
        for row in results
    ]

