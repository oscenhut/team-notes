from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user import UserRepository
from app.services.auth import AuthService

class UserService:
    def __init__(self, user_repo: Optional[UserRepository] = None):
        self.user_repo = user_repo or UserRepository()
        self.auth_service = AuthService()

    # def create_user(self, db: Session, *, email: str, name: str, password: str) -> User:
    #     """Business logic to register a new user with hashed credentials."""
    #     hashed_password = self.auth_service.get_password_hash(password)
    #     try:
    #         return self.user_repo.create(
    #             db, 
    #             email=email, 
    #             name=name, 
    #             password_hash=hashed_password
    #         )
    #     except Exception:
    #         db.rollback()
    #         raise HTTPException(
    #             status_code=status.HTTP_400_BAD_REQUEST,
    #             detail="User with this email already exists or invalid data provided."
    #         )

    def create_user(self, db: Session, *, email: str, name: str, password: str) -> User:
        """Business logic to register a new user with hashed credentials."""
        hashed_password = self.auth_service.get_password_hash(password)
        
        # TEMPORARILY REMOVE try...except to see the real error traceback
        return self.user_repo.create(
            db, 
            email=email, 
            name=name, 
            password_hash=hashed_password
        )

    def get_user_by_id(self, db: Session, user_id: int) -> User:
        """Retrieve a user by ID, raising 404 if not found."""
        user = self.user_repo.getById(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return user

    def search_users(self, db: Session, query_str: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Search users matching name or email."""
        return self.user_repo.search(db, query_str=query_str, skip=skip, limit=limit)