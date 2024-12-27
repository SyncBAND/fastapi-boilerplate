from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.app import router
from src.core.cache import Cache, CustomKeyMaker, RedisBackend
from src.core.config import settings
from src.core.database import Base, engines
from src.core.dependencies import AuthenticationRequired, Logging
from src.core.exceptions import CustomException
from src.core.middlewares import (
    AuthBackend,
    AuthenticationMiddleware,
    ResponseLoggerMiddleware,
    SQLAlchemyMiddleware,
)


# -------------- cache --------------
def init_cache():
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())


# -------------- database --------------
async def create_tables():
    """
    Create all tables defined in the SQLAlchemy Base.
    This uses the writer engine to ensure DDL commands are applied correctly.
    """
    async with engines["writer"].begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


def init_listeners(app_: FastAPI) -> None:
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "detail": exc.detail},
        )


# -------------- lifespan --------------
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup tasks
    await create_tables()
    init_cache()

    yield  # Hand over control to the application


# -------------- routers --------------
def init_routers(app_: FastAPI) -> None:
    app_.include_router(router)


# -------------- middleware --------------
def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
        ),
        Middleware(SQLAlchemyMiddleware),
        Middleware(ResponseLoggerMiddleware),
    ]
    return middleware


# ----------- application -----------
def create_app() -> FastAPI:
    app_ = FastAPI(
        lifespan=lifespan,
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        docs_url=None if settings.ENVIRONMENT == "production" else "/docs",
        redoc_url=None if settings.ENVIRONMENT == "production" else "/redoc",
        dependencies=[Depends(Logging), Depends(AuthenticationRequired)],
        middleware=make_middleware()
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    return app_


app = create_app()
