from datetime import date

import pandas as pd
from sqlmodel import Session

from app.database import engine
from app.models import Sale

df = pd.read_csv("data\FMCG_2022_2024.csv")

# Convert Datatypes for convinence
df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y").dt.date
df["promotion_flag"] = df["promotion_flag"].astype(bool)

with Session(engine) as session:
    sales = [
        Sale(
            date=row.date,
            sku=row.sku,
            brand=row.brand,
            segment=row.segment,
            category=row.category,
            channel=row.channel,
            region=row.region,
            pack_type=row.pack_type,
            price_unit=row.price_unit,
            promotion_flag=row.promotion_flag,
            delivery_days=row.delivery_days,
            stock_available=row.stock_available,
            delivered_qty=row.delivered_qty,
            units_sold=row.units_sold,            
        )
        for row in df.itertuples(index=False)
    ]

    session.add_all(sales)
    session.commit()

print(f"Imported {len(sales)} records successfully!")
