from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import User
from app.security import hash_password


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    email: str,
    password: str,
    session: Session = Depends(get_session)
):
    existing_user = session.exec(
        select(User).where(User.email == email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        email=email,
        hashed_password=hash_password(password),
        role="viewer"
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "email": user.email,
        "role": user.role
    }