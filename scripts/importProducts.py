from sqlmodel import Session
import pandas as pd

from app.database import engine
from app.models import Product

df = pd.read_csv("D:\\EmamiIntern\\CAPSTONE1\\SalesAnalyticsAPI\\data\\Products.csv")

# Convert MRP to numeric (#REF! becomes NaN)
df["MRP"] = pd.to_numeric(df["MRP"], errors="coerce")

# Remove rows with invalid MRP
df = df.dropna(subset=["MRP"])

# Convert Discount
df["Discount"] = (
    df["Discount"]
      .str.replace("% off", "", regex=False)
      .astype(int)
)


with Session(engine) as session:

    for _, row in df.iterrows():

        product = Product(
            product_id=row["Product ID"],
            product_name=row["Product Name"],

            brand_name=row["BrandName"],
            brand_desc=row["Brand Desc"],

            category=row["Category"],
            product_size=row["Product Size"],

            currency=row["Currancy"],

            mrp=row["MRP"],
            sell_price=row["SellPrice"],
            discount=row["Discount"]
        )

        session.add(product)

    session.commit()

print(f"Imported {len(df)} products successfully!")