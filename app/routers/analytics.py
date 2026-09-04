from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlmodel import Session, select
from sqlalchemy import func

from app.database import get_session
from app.models import Sale, User
from app.saleSchema import (
    KPIResponses,
    SalesTrendResponse,
    SalesByRegionResponses,
    SalesByCategory,
    TopProductResponse,
    Granularity,
    ByChannel,
)
from app.security import get_current_user

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


def validate_date_range(
    start_date: Optional[date],
    end_date: Optional[date],
):
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date cannot be later than end_date."
        )


def apply_date_filter(
    query,
    start_date: Optional[date],
    end_date: Optional[date],
):
    if start_date is not None:
        query = query.where(Sale.date >= start_date)

    if end_date is not None:
        query = query.where(Sale.date <= end_date)

    return query


@router.get(
    "/kpis",
    response_model=KPIResponses,
    summary="Get business KPIs",
    description="Retrieve dashboard KPIs for the selected date range."
)
def get_kpis(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    validate_date_range(start_date, end_date)

    query = select(
        func.count(Sale.id),
        func.sum(Sale.price_unit * Sale.units_sold),
    )

    query = apply_date_filter(
        query,
        start_date,
        end_date,
    )

    result = session.exec(query).one()

    orders = result[0] or 0
    revenue = result[1] or 0

    aov = revenue / orders if orders else 0

    category_query = (
        select(
            Sale.category,
            func.sum(Sale.units_sold).label("units_sold")
        )
    )

    category_query = apply_date_filter(
        category_query,
        start_date,
        end_date,
    )

    category_query = (
        category_query
        .group_by(Sale.category)
        .order_by(
            func.sum(Sale.units_sold).desc()
        )
        .limit(1)
    )

    category_result = session.exec(category_query).first()

    top_category = (
        category_result[0]
        if category_result
        else "N/A"
    )

    return KPIResponses(
        total_revenue=round(revenue, 2),
        orders=orders,
        aov=round(aov, 2),
        top_category=top_category,
    )


@router.get(
    "/top",
    response_model=list[TopProductResponse],
    summary="Get top-selling products",
    description="Retrieve top-selling products for the selected date range."
)
def get_top_products(
    session: Session = Depends(get_session),
    limit: int = Query(default=10, ge=1, le=100),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    validate_date_range(start_date, end_date)

    query = select(
        Sale.sku,
        func.sum(Sale.units_sold).label("units_sold"),
    )

    query = apply_date_filter(
        query,
        start_date,
        end_date,
    )

    query = (
        query
        .group_by(Sale.sku)
        .order_by(
            func.sum(Sale.units_sold).desc()
        )
        .limit(limit)
    )

    results = session.exec(query).all()

    return [
        TopProductResponse(
            product_id=row[0],
            product_name=row[0],
            units_sold=row[1],
        )
        for row in results
    ]


@router.get(
    "/sales/trend",
    response_model=list[SalesTrendResponse],
    summary="Get sales trend",
    description="Get sales trends grouped by daily, weekly, monthly, or yearly intervals."
)
def get_sales_trend(
    session: Session = Depends(get_session),
    granularity: Granularity = Granularity.daily,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    validate_date_range(start_date, end_date)

    period_map = {
        Granularity.daily: "day",
        Granularity.weekly: "week",
        Granularity.monthly: "month",
        Granularity.yearly: "year",
    }

    period = period_map[granularity]

    query = select(
        func.date_trunc(
            period,
            Sale.date
        ).label("period"),

        func.sum(
            Sale.units_sold
        ).label("units_sold"),

        func.count(
            Sale.id
        ).label("orders"),

        func.sum(
            Sale.price_unit * Sale.units_sold
        ).label("total_revenue"),

        func.sum(
            Sale.delivered_qty
        ).label("total_delivered"),
    )

    query = apply_date_filter(
        query,
        start_date,
        end_date,
    )

    query = (
        query
        .group_by("period")
        .order_by("period")
    )

    results = session.exec(query).all()

    return [
        SalesTrendResponse(
            date=row.period.date(),
            orders=row.orders or 0,
            units_sold=row.units_sold or 0,
            total_revenue=round(
                row.total_revenue or 0,
                2
            ),
            total_delivered_qty=row.total_delivered or 0,
        )
        for row in results
    ]


@router.get(
    "/sales/by-region",
    response_model=list[SalesByRegionResponses],
    summary="Get sales by region",
    description="Get total units sold grouped by region."
)
def get_sales_by_region(
    session: Session = Depends(get_session),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    validate_date_range(start_date, end_date)

    query = select(
        Sale.region,
        func.sum(Sale.units_sold)
    )

    query = apply_date_filter(
        query,
        start_date,
        end_date,
    )

    query = (
        query
        .group_by(Sale.region)
        .order_by(
            func.sum(Sale.units_sold).desc()
        )
    )

    results = session.exec(query).all()

    return [
        SalesByRegionResponses(
            region=row[0],
            units_sold=row[1],
        )
        for row in results
    ]


@router.get(
    "/sales/by-category",
    response_model=list[SalesByCategory],
    summary="Get sales by category",
    description="Get total units sold grouped by product category."
)
def get_sales_by_category(
    session: Session = Depends(get_session),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    validate_date_range(start_date, end_date)

    query = select(
        Sale.category,
        func.sum(Sale.units_sold)
    )

    query = apply_date_filter(
        query,
        start_date,
        end_date,
    )

    query = (
        query
        .group_by(Sale.category)
        .order_by(
            func.sum(Sale.units_sold).desc()
        )
    )

    results = session.exec(query).all()

    return [
        SalesByCategory(
            category=row[0],
            units_sold=row[1],
        )
        for row in results
    ]


@router.get(
    "/sales/by-channel",
    response_model=list[ByChannel],
    summary="Get sales by channel",
    description="Retrieve revenue, delivered quantity and average selling price grouped by sales channel."
)
def get_by_channel(
    session: Session = Depends(get_session),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    validate_date_range(start_date, end_date)

    query = select(
        Sale.channel,
        func.sum(
            Sale.price_unit * Sale.units_sold
        ),
        func.sum(Sale.delivered_qty),
        func.avg(Sale.price_unit),
    )

    query = apply_date_filter(
        query,
        start_date,
        end_date,
    )

    query = query.group_by(Sale.channel)

    results = session.exec(query).all()

    return [
        ByChannel(
            channel=row[0],
            total_revenue=round(row[1] or 0, 2),
            total_delivered_qty=row[2] or 0,
            average_price=round(row[3] or 0, 2),
        )
        for row in results
    ]