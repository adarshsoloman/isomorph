from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ...db.session import get_db
from ...config import settings

router = APIRouter()

@router.get("/")
async def health_check(db: Session = Depends(get_db)):
    """
    Check API health, database connectivity, and pipeline version.
    """
    try:
        # Check DB connectivity
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    return {
        "status": "ok",
        "pipeline_version": settings.PIPELINE_VERSION,
        "database": db_status,
        "environment": settings.ENVIRONMENT
    }
