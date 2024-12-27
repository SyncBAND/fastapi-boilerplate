from typing import Optional, Tuple

from jose import JWTError, jwt
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import (
    AuthenticationMiddleware as BaseAuthenticationMiddleware,
)
from starlette.requests import HTTPConnection

from src.app.auth.schemas import CurrentUserSchema
from src.core.config import settings


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> Tuple[bool, Optional[CurrentUserSchema]]:
        current_user = CurrentUserSchema()

        authorization: str = conn.headers.get("Authorization")

        if not authorization:
            return False, current_user

        try:
            scheme, token = authorization.split(" ")
            if scheme.lower() != "bearer" or not token:
                return False, current_user

            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
            user_id = payload.get("user_id")
            if not user_id:
                return False, current_user

            current_user.id = user_id
            current_user.is_authenticated = True
        except (JWTError, ValueError):
            return False, current_user

        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
