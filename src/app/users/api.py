from typing import Callable

from fastapi import APIRouter, Depends

from src.app.users.models import User, UserPermission
from src.app.users.queries import UserQuery
from src.app.users.schemas import UserDetailSchema
from src.core.factory import Factory
from src.core.dependencies.current_user import get_current_user
from src.core.dependencies.permissions import Permissions


user_router = APIRouter(tags=["Users"])


@user_router.get("")
async def get_users(
    user_query: UserQuery = Depends(Factory().get_user_query),
    assert_access: Callable = Depends(Permissions(UserPermission.READ)),
) -> list[UserDetailSchema]:
    users = await user_query.get_all()
    assert_access(resource=users)
    return users


@user_router.get("/me")
def get_user(user: User = Depends(get_current_user)) -> UserDetailSchema:
    return user
