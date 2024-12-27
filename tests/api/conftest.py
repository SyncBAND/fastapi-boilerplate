# pylint: disable=redefined-outer-name
from typing import Any, Generator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient

from src.core.database import async_get_session
from src.core.server import create_app


@pytest.fixture(scope="session")
def app() -> Generator[FastAPI, Any, None]:
    """
    Create a new FastAPI app
    """
    _app = create_app()

    yield _app


@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI, db_session) -> AsyncClient:
    """
    Create a new FastAPI AsyncClient
    """

    async def _async_get_session():
        return db_session

    app.dependency_overrides[async_get_session] = _async_get_session

    async with AsyncClient(app=app, base_url="http://test") as _client:
        yield _client
