from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from sqlalchemy import func
from typing import Optional

from app.database import get_session
from app.models import Sale
from SalesAnalyticsAPI.app.saleSchema import *

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

@router.get("/top", response_model=list[TopProductResponse], summary="Get top-selling products", description="Retrieve the top selling products ranked by total units sold.")
def get_top_products(session: Session = Depends(get_session), 
    limit: int = Query(default=10, le=100),
    granularity: Granularity = Granularity.daily, 
    year: Optional[int] = None, 
    month: Optional[int] = None
):
    period_map = {
            Granularity.daily: "day",
            Granularity.weekly: "week",
            Granularity.monthly: "month",
            Granularity.yearly: "year"
        }
    
    period = period_map[granularity]
    
    if year is not None and year not in (2022, 2023, 2024):
        raise HTTPException(
            status_code=400,
            detail="Year must be between 2022 and 2024."
        )

    if month is not None and year is None:
        raise HTTPException(
            status_code=400,
            detail="Please specify a year when filtering by month."
        )

    if month is not None and not 1 <= month <= 12:
        raise HTTPException(
            status_code=400,
            detail="Month must be between 1 and 12."
        )

    query = (
        select(
            func.date_trunc(period, Sale.date).label("period"),
            Sale.brand,
            func.sum(Sale.units_sold)
        ).group_by(func.date_trunc(period, Sale.date), Sale.brand).order_by(func.sum(Sale.units_sold).desc()).limit(limit)
    )

    if year is not None:
        query = query.where(func.extract("year", Sale.date) == year)

    if month is not None:
        query = query.where(func.extract("month", Sale.date) == month)

    query = (
        query
        .group_by("period")
        .order_by("period")
    )
    results = session.exec(query).all()

    return [
        TopProductResponse(
            date = row[0],
            brand = row[1],
            units_sold= row[2]
        )
        for row in results
    ]

@router.get("/sales/trend", 
    response_model=list[SalesTrendResponse], 
    summary="Get sales trend", 
    description="""
    Get sales trends grouped by daily, weekly, monthly, or yearly intervals.

    Examples:
    - Whole year month-wise:
      /sales/trend?year=2024&granularity=monthly

    - Selected month day-wise:
      /sales/trend?year=2024&month=3&granularity=daily

    - Selected month week-wise:
      /sales/trend?year=2024&month=3&granularity=weekly

    - Complete dataset year-wise:
      /sales/trend?granularity=yearly
    """
)
def get_sales_trend(
    session: Session = Depends(get_session), 
    granularity: Granularity = Granularity.daily, 
    year: Optional[int] = None, 
    month: Optional[int] = None
):
    period_map = {
        Granularity.daily: "day",
        Granularity.weekly: "week",
        Granularity.monthly: "month",
        Granularity.yearly: "year"
    }

    period = period_map[granularity]

    if year is not None and year not in (2022, 2023, 2024):
        raise HTTPException(
            status_code=400,
            detail="Year must be between 2022 and 2024."
        )

    if month is not None and year is None:
        raise HTTPException(
            status_code=400,
            detail="Please specify a year when filtering by month."
        )

    if month is not None and not 1 <= month <= 12:
        raise HTTPException(
            status_code=400,
            detail="Month must be between 1 and 12."
        )

    if month is not None and granularity in (Granularity.monthly, Granularity.yearly):
        raise HTTPException(
        status_code=400,
        detail="For a selected month, granularity must be daily or weekly."
    )


    query = (
        select(
            func.date_trunc(period, Sale.date).label("period"),
            func.sum(Sale.units_sold).label("units_sold"),
            func.sum(Sale.price_unit * Sale.units_sold).label("total_revenue"),
            func.sum(Sale.delivered_qty).label("total_delivered")
        )
    )

    if year is not None:
        query = query.where(func.extract("year", Sale.date) == year)

    if month is not None:
        query = query.where(func.extract("month", Sale.date) == month)

    query = (
        query
        .group_by("period")
        .order_by("period")
    )
    results = session.exec(query).all()

    return [
        SalesTrendResponse(
            date=row.period.date(),
            units_sold=row.units_sold or 0,
            total_revenue=round(row.total_revenue or 0,2),
            total_delivered_qty=row.total_delivered or 0
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

@router.get("/sales/by-channel", response_model=list[ByChannel], summary="Get sales by channel", description="Retrieve revenue, delivered quantity and average selling price grouped by sales channel.")
def get_by_channel(session: Session = Depends(get_session)):
    query = (
        select(
            Sale.channel,
            func.sum(Sale.price_unit * Sale.units_sold),
            func.sum(Sale.delivered_qty),
            func.avg(Sale.price_unit)
        ).group_by(Sale.channel)
    )

    result = session.exec(query).all()

    return [
        ByChannel(
            channel=row[0],
            total_revenue=round(row[1], 2),
            total_delivered_qty=row[2],
            average_price=round(row[3], 2)
        )
        for row in result
    ]