from fastapi import APIRouter, Depends

from src.app.auth.queries import AuthQuery
from src.app.auth.schemas import LoginUserSchema, RegisterUserSchema, TokenSchema
from src.app.users.schemas import UserSchema
from src.core.factory import Factory


auth_router = APIRouter(tags=["Auth"])


@auth_router.post("/register", status_code=201)
async def register_user(
    register_user_request: RegisterUserSchema,
    auth_query: AuthQuery = Depends(Factory().get_auth_query),
) -> UserSchema:
    return await auth_query.register(
        email=register_user_request.email,
        password=register_user_request.password,
        firstname=register_user_request.firstname,
        lastname=register_user_request.lastname,
    )


@auth_router.post("/login")
async def login_user(
    login_user_request: LoginUserSchema,
    auth_query: AuthQuery = Depends(Factory().get_auth_query),
) -> TokenSchema:
    return await auth_query.login(
        email=login_user_request.email,
        password=login_user_request.password
    )
