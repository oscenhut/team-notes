from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, or_

from app.models.user import User

class UserRepository:
    def create(
        self, 
        db: Session, 
        *, 
        email: str, 
        name: str, 
        password_hash: str
    ) -> User:
        """Create and persist a new user record."""
        db_user = User(
            email=email,
            name=name,
            password_hash=password_hash
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def getById(self, db: Session, user_id: int) -> Optional[User]:
        """Retrieve a single user by their primary key ID."""
        stmt = select(User).where(User.id == user_id)
        return db.scalars(stmt).first()

    def search(self, db: Session, query_str: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Search users by name or email matching the query string."""
        search_pattern = f"%{query_str}%"
        stmt = (
            select(User)
            .where(
                or_(
                    User.name.ilike(search_pattern),
                    User.email.ilike(search_pattern)
                )
            )
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())