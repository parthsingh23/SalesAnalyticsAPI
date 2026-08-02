from sqlmodel import SQLModel
from datetime import date
from enum import Enum

class KPIResponses(SQLModel):
    total_records: int
    total_units_sold: int
    total_delivered_qty: int
    total_revenue: float
    average_price: float
    unique_products: int

class SalesTrendResponse(SQLModel):
    date: date
    units_sold: int
    total_revenue: float
    total_delivered_qty: int

class SalesByRegionResponses(SQLModel):
    region: str
    units_sold: int

class SalesByCategory(SQLModel):
    category: str
    units_sold: int

class TopProductResponse(SQLModel):
    date: date
    brand: str
    units_sold: int

class Granularity(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    yearly = "yearly"

class ByChannel(SQLModel):
    channel: str
    total_revenue: float
    total_delivered_qty: int
    average_price: float
