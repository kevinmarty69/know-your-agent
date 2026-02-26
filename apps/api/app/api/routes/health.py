from fastapi import APIRouter
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import SessionLocal, redis_client

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    summary="Health Check",
    description="Returns API, PostgreSQL and Redis health status.",
)
def health_check() -> dict[str, str]:
    db_status = "ok"
    redis_status = "ok"

    try:
        with SessionLocal() as session:
            session.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db_status = "error"

    try:
        redis_client.ping()
    except RedisError:
        redis_status = "error"

    status = "ok" if db_status == "ok" and redis_status == "ok" else "degraded"
    return {"status": status, "db": db_status, "redis": redis_status}
