from sqlmodel import SQLModel, Field
from datetime import date


class Sale(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    date: date

    sku: str
    brand: str
    segment: str
    category: str
    channel: str
    region: str
    pack_type: str

    price_unit: float
    promotion_flag: bool

    delivery_days: int
    stock_available: int
    delivered_qty: int
    units_sold: int
