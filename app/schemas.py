from sqlmodel import SQLModel
from datetime import date

# Analytics Schema
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

"""---------------------------------------------------------"""


# Products Schema

class ProductCreate(SQLModel):
    product_id: str
    product_name: str

    brand_name: str
    brand_desc: str

    category: str
    product_size: str

    currency: str

    mrp: float
    sell_price: float
    discount: int


class ProductRead(ProductCreate):
    id: int


class ProductUpdate(SQLModel):
    product_name: str | None = None
    brand_name: str | None = None
    brand_desc: str | None = None
    category: str | None = None
    product_size: str | None = None
    currency: str | None = None
    mrp: float | None = None
    sell_price: float | None = None
    discount: int | None = None
