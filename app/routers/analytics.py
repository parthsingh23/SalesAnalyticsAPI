from fastapi import APIRouter

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

@router.get("/kpis")
def get_kpis():
    return {"message": "KPI endpoint"}