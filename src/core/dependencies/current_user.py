from fastapi import Depends, Request

from src.app.users.queries import UserQuery
from src.core.factory import Factory


async def get_current_user(
    request: Request,
    user_query: UserQuery = Depends(Factory().get_user_query),
):
    """
    Get the current authenticated user from the request.
    """
    return await user_query.get_by_id(request.user.id)
