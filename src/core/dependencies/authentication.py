from fastapi import Depends, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.exceptions.base import CustomException


class AuthenticationRequiredException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = status.HTTP_401_UNAUTHORIZED
    detail = "Authentication required"


class AuthenticationRequired:
    public_routes = {"/api/health", "/api/login", "/api/register", "/docs", "/redoc"}
    def __init__(
        self,
        request: Request,
        token: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    ):
        # Skip authentication for public routes
        if request.url.path in self.public_routes:
            return
        if not token:
            raise AuthenticationRequiredException()
