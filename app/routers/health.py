from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import get_db

router = APIRouter(prefix="/health", tags=["Health & Diagnostics"])


@router.get("", status_code=status.HTTP_200_OK)
def health_check():
    """Basic health check endpoint returning service status and version."""
    return {
        "status": "healthy",
        "service": "TeamNotes API",
        "version": "1.0.0"
    }


@router.get("/liveness", status_code=status.HTTP_200_OK)
def liveness_check():
    """Liveness probe to confirm the container/application process is running."""
    return {"status": "alive"}


@router.get("/readiness", status_code=status.HTTP_200_OK)
def readiness_check(db: Session = Depends(get_db)):
    """Readiness probe checking application readiness and active database connectivity."""
    try:
        # Execute a lightweight query to verify the database connection pool is healthy
        db.execute(text("SELECT 1"))
        return {
            "status": "ready",
            "database": "connected"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection check failed: {str(e)}"
        )