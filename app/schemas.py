from sqlmodel import SQLModel, Field
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
    product_id: str = Field(min_length=3, max_length=20)
    product_name: str = Field(min_length=2, max_length=100)

    brand_name: str = Field(min_length=2)
    brand_desc: str

    category: str
    product_size: str

    currency: str = Field(min_length=3, max_length=3)

    mrp: float = Field(gt=0)
    sell_price: float = Field(gt=0)
    discount: int = Field(ge=0, le=100)


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


