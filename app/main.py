from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import create_db_and_table
from app.models import Sale

@asynccontextmanager
async def startup(app: FastAPI):
    create_db_and_table()
    yield

app = FastAPI(lifespan=startup)

@app.get("/")
def root():
    return {"message": "Sales Analytics API"}