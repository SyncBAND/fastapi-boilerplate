import uvicorn

from src.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        app="src.core.server:app",
        reload=settings.ENVIRONMENT != "production",
        workers=1,
    )
