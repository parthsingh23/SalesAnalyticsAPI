from sqlmodel import SQLModel
from datetime import date
from enum import Enum

class KPIResponses(SQLModel):
    total_revenue: float
    orders: int
    aov: float
    top_category: str

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
    product_id: str
    product_name: str
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
