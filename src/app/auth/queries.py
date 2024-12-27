from pydantic import EmailStr

from sqlalchemy.exc import NoResultFound

from src.app.auth.schemas import TokenSchema
from src.app.users.models import User
from src.core.queries import BaseQuery
from src.core.database import Propagation, Transactional
from src.core.exceptions import BadRequestException, UnauthorizedException
from src.core.security import JWTHandler, PasswordHandler


class AuthQuery(BaseQuery[User]):
    """
    Query for handling authentication-related operations.
    """

    @Transactional(propagation=Propagation.REQUIRED)
    async def register(self, email: EmailStr, password: str, firstname: str, lastname: str) -> User:
        """
        Register a new user.
        
        :param email: User's email
        :param password: User's password
        :param firstname: User's firstname
        :param lastname: User's lastname
        :return: Created user instance
        :raises BadRequestException: If user already exists
        """
        # Check if user exists with email
        try:
            await self.get_by(field="email", value=email, unique=True)
            raise BadRequestException("User already exists with this email")
        except NoResultFound:
            ...

        # Hash password and create user
        hashed_password = PasswordHandler.hash(password)
        return await self.create(
            {
                "email": email,
                "password": hashed_password,
                "firstname": firstname,
                "lastname": lastname,
            }
        )

    async def login(self, email: EmailStr, password: str) -> TokenSchema:
        """
        Authenticate a user and return access tokens.
        
        :param email: User's email
        :param password: User's password
        :return: TokenSchema object containing access and refresh tokens
        :raises BadRequestException: If credentials are invalid
        """
        try:
            user = await self.get_by(field="email", value=email, unique=True)
        except NoResultFound as e:
            raise BadRequestException("Invalid credentials") from e

        if not PasswordHandler.verify(user.password, password):
            raise BadRequestException("Invalid credentials")

        return TokenSchema(
            access_token=JWTHandler.encode(payload={"user_id": str(user.id)}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )

    async def refresh_token(self, access_token: str, refresh_token: str) -> TokenSchema:
        """
        Refresh an existing access token.
        
        :param access_token: Current access token
        :param refresh_token: Current refresh token
        :return: New TokenSchema object
        :raises UnauthorizedException: If refresh token is invalid
        """
        token = JWTHandler.decode(access_token)
        refresh_token_decoded = JWTHandler.decode(refresh_token)

        if refresh_token_decoded.get("sub") != "refresh_token":
            raise UnauthorizedException("Invalid refresh token")

        return TokenSchema(
            access_token=JWTHandler.encode(payload={"user_id": token.get("user_id")}),
            refresh_token=JWTHandler.encode(payload={"sub": "refresh_token"}),
        )
