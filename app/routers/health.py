from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.cache import redis_client
from sqlalchemy import text

router = APIRouter(
    prefix="/health",
    tags = ["Health"],
)

@router.get("/")
def health_check(db:Session=Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "error"

    try:
        redis_client.ping()
        redis_status = "ok"
    except Exception:
        redis_status = "error"

    return{
        "status":"ok" if db_status=="ok" and redis_status=="ok" else "degraded",
        "database": db_status,
        "redis": redis_status,
    }