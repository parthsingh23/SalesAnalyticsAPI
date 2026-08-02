from sqlmodel import SQLModel, Field
from pydantic import field_validator
from datetime import date
from enum import Enum

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

"""---------------------------------------------------------"""


# Products Schema

class ProductCreate(SQLModel):
    product_id: str = Field(min_length=3, max_length=20)
    product_name: str = Field(min_length=2, max_length=100)

    brand_name: str = Field(min_length=2)
    brand_desc: str

    category: str
    product_size: str

    currency: str

    mrp: float = Field(gt=0)
    sell_price: float = Field(gt=0)
    # discount: int = Field(ge=0, le=100)

    @field_validator(
        "product_id",
        "product_name",
        "brand_name",
        "brand_desc",
        "category",
        "product_size",
        "currency"
    )
    @classmethod
    def validate_string_fields(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("This field cannot be empty.")

        if value.lower() == "string":
            raise ValueError("Please provide a valid value instead of 'string'.")

        return value


class ProductBase(SQLModel):
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

class ProductRead(ProductBase):
    id: int

class ProductUpdate(SQLModel):
    product_name: str | None = Field(default=None, min_length=2, max_length=100)
    brand_name: str | None = Field(default=None, min_length=2)
    brand_desc: str | None = None
    category: str | None = None
    product_size: str | None = None
    currency: str | None = None
    mrp: float | None = Field(default=None, gt=0)
    sell_price: float | None = Field(default=None, gt=0)



