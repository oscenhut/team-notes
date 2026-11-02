from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.config import settings

# SQLite-specific optimization for multi-threaded/FastAPI request handling
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy 2.0 database models."""
    pass

def get_db():
    """FastAPI dependency that provides a transactional SQLAlchemy session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()