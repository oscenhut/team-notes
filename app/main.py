from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import auth, user, team, note, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for startup and shutdown."""
    Base.metadata.create_all(bind=engine)
    yield

    # Do not dispose the shared engine here.
    # The engine lifecycle is managed separately.

app = FastAPI(
    title="TeamNotes API",
    description="A production-ready, multi-tenant TeamNotes API built with FastAPI and SQLAlchemy 2.0.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS Middleware (Adjust allow_origins for your specific production frontend domains)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API Routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(team.router)
app.include_router(note.router)
app.include_router(health.router)

@app.get("/", tags=["Health Check"])
def health_check():
    """Root health check endpoint to verify service status."""
    return {
        "status": "healthy",
        "service": "TeamNotes API",
        "version": "1.0.0"
    }