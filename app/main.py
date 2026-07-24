from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_db_and_table
from app.models import Sale

from app.routers import analytics, products

@asynccontextmanager
async def startup(app: FastAPI):
    create_db_and_table()
    yield

app = FastAPI(lifespan=startup, 
    title="Sales Analytics API", 
    description="Backend API for Sales Analytics Dashboard",
    version="1.0.0"
)

app.include_router(analytics.router)
app.include_router(products.router)

@app.get("/")
def root():
    return {"message": "Sales Analytics API"}