from fastapi import APIRouter

from src.core.api import core_router
from src.app.auth.api import auth_router
from src.app.moods.api import mood_router
from src.app.users.api import user_router

router = APIRouter(prefix="/api")
router.include_router(core_router, prefix="/health")
router.include_router(auth_router, prefix="")
router.include_router(mood_router, prefix="/moods")
router.include_router(user_router, prefix="/users")
