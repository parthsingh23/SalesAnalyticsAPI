from sqlmodel import SQLModel
from datetime import date

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

class SalesByRegionResponses(SQLModel):
    region: str
    units_sold: int

class SalesByCategory(SQLModel):
    category: str
    units_sold: int

class TopProductResponse(SQLModel):
    sku: str
    brand: str
    units_sold: int