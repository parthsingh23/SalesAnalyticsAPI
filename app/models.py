from sqlmodel import SQLModel, Field
from datetime import date


class Sale(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sale_date: date
    sku: str = Field(min_length=2, max_length=6)
    