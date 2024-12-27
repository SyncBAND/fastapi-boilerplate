from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from src.core.config import settings
from src.core.schemas import Health
from src.core.database.session import async_get_session

core_router = APIRouter(tags=["Core"])


@core_router.get("", dependencies=[])
async def health(db_connection: Annotated[Session, Depends(async_get_session)]) -> Health:
    """
    Health check endpoint that now includes database connectivity check.

    Attempts to make a simple query to the database to ensure connectivity.

    Returns:
        dict[str, str]: A dictionary with the status of the application and database connectivity.
    """
    try:
        # Attempt a simple query to check database connectivity
        # The specific query can be adjusted based on your database schema.
        # Here, we're just checking if we can execute a simple SELECT.
        await db_connection.execute(text("SELECT 1"))
    except OperationalError:
        # If database connection fails, catch the error and return an appropriate response
        return Health(version=settings.APP_VERSION, status="Healthy", database="Unhealthy")

    return Health(version=settings.APP_VERSION, status="Healthy", database="Healthy")
