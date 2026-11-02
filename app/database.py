import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import StaticPool
from app.config import settings

def get_database_url():
    url = os.getenv("DATABASE_URL") or settings.DATABASE_URL
    # Force SQLite shared-cache URI memory so all connections and threads share the same tables
    if url and ("sqlite" in url and ":memory:" in url):
        return "sqlite:///file:test_db?mode=memory&cache=shared"
    return url

_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        url = get_database_url()
        is_sqlite_mem = "sqlite" in url and "mode=memory" in url
        
        connect_args = {"check_same_thread": False}
        if is_sqlite_mem:
            connect_args["uri"] = True

        _engine = create_engine(
            url,
            connect_args=connect_args,
            poolclass=StaticPool if is_sqlite_mem else None,
            pool_pre_ping=True
        )
    return _engine

def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine()
        )
    return _SessionLocal

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy 2.0 database models."""
    pass

# def get_db():
#     SessionMaker = get_session_local()

#     print(
#         "REQUEST ENGINE ID:",
#         id(SessionMaker.kw["bind"])
#     )

#     db = SessionMaker()

#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy import inspect

def get_db():
    SessionMaker = get_session_local()
    db_engine = get_engine()

    with db_engine.connect() as connection:
        print(
            "TABLES AT REQUEST:",
            inspect(connection).get_table_names()
        )

    db = SessionMaker()

    try:
        yield db
    finally:
        db.close()
        

# Backward compatibility proxies for engine and SessionLocal
class _LazyEngineProxy:
    def __getattr__(self, name):
        return getattr(get_engine(), name)

class _LazySessionLocalProxy:
    def __call__(self, *args, **kwargs):
        return get_session_local()(*args, **kwargs)
    def __getattr__(self, name):
        return getattr(get_session_local(), name)

engine = _LazyEngineProxy()
SessionLocal = _LazySessionLocalProxy()