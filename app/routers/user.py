from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])

def get_user_service() -> UserService:
    return UserService()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: UserCreate,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    """Register a new user with email, name, and secure password hashing."""
    return user_service.create_user(
        db,
        email=user_in.email,
        name=user_in.name,
        password=user_in.password
    )


@router.get("", response_model=List[UserResponse])
def search_users(
    q: Optional[str] = Query(None, description="Search query string for user name or email"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    """Search or list users matching name or email criteria with pagination."""
    return user_service.search_users(db, query_str=q or "", skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    user_service: UserService = Depends(get_user_service)
):
    """Retrieve a specific user by their unique ID."""
    return user_service.get_user_by_id(db, user_id=user_id)