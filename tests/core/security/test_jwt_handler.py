# pylint: disable=redefined-outer-name
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest
from jose import JWTError, jwt

from src.core.security.jwt import JWTDecodeError, JWTHandler


class MockSettings:
    SECRET_KEY = "secret_key"
    ALGORITHM = "HS256"
    JWT_EXPIRE_MINUTES = 10


@pytest.fixture
def mock_settings() -> MockSettings:
    """Create a mock settingsuration object for testing.

    Returns:
        MockSettings: A mock configuration object with test settings
    """
    return MockSettings()


@pytest.fixture
def mock_payload() -> Dict[str, Any]:
    """Create a mock JWT payload for testing.

    Returns:
        Dict[str, Any]: A dictionary containing test JWT claims
    """
    return {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": 1516239022
    }


@pytest.fixture
def mock_token(mock_payload: Dict[str, Any], mock_settings: MockSettings) -> str:
    """
    Generate a mock JWT token for testing.

    Args:
        mock_payload: The base JWT payload to use
        mock_settings: Settingsuration object containing JWT settings

    Returns:
        str: An encoded JWT token
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=mock_settings.JWT_EXPIRE_MINUTES)
    payload = mock_payload.copy()
    payload.update({"exp": expire})

    return jwt.encode(
        payload, mock_settings.SECRET_KEY, algorithm=mock_settings.ALGORITHM
    )


@pytest.fixture
def mock_expired_token(mock_payload, mock_settings):
    expire = (
        datetime.now(timezone.utc)
        - timedelta(minutes=mock_settings.JWT_EXPIRE_MINUTES)
        - timedelta(seconds=10)
    )
    payload = mock_payload.copy()
    payload.update({"exp": expire})
    return jwt.encode(
        payload, mock_settings.SECRET_KEY, algorithm=mock_settings.ALGORITHM
    )


@pytest.fixture
def mock_decode_token(mock_settings, mock_payload):
    return jwt.encode(
        mock_payload, mock_settings.SECRET_KEY, algorithm=mock_settings.ALGORITHM
    )


@pytest.fixture
def mock_handler(mock_settings):
    jwt_handler = JWTHandler
    jwt_handler.secret_key = mock_settings.SECRET_KEY
    jwt_handler.algorithm = mock_settings.ALGORITHM
    jwt_handler.expire_minutes = mock_settings.JWT_EXPIRE_MINUTES

    return jwt_handler


class TestJWTHandler:
    @patch("src.core.security.jwt.settings", MagicMock(return_value=mock_settings))
    def test_encode(self, mock_payload, mock_handler):
        token = mock_handler.encode(mock_payload)
        assert token is not None
        assert isinstance(token, str)

    @patch("src.core.security.jwt.settings", MagicMock(return_value=mock_settings))
    def test_decode(self, mock_token, mock_payload, mock_handler):
        decoded = mock_handler.decode(mock_token)
        assert decoded is not None
        assert isinstance(decoded, dict)
        assert decoded.pop("exp") is not None
        assert decoded == mock_payload

    @patch("src.core.security.jwt.settings", MagicMock(return_value=mock_settings))
    def test_decode_expired(self, mock_expired_token, mock_handler):
        decoded = mock_handler.decode_expired(mock_expired_token)
        assert decoded is not None
        assert isinstance(decoded, dict)

    @patch("src.core.security.jwt.settings", MagicMock(return_value=mock_settings))
    def test_decode_error(self, mock_token, mock_handler):
        with pytest.raises(JWTDecodeError):
            with patch.object(jwt, "decode", side_effect=JWTError):
                mock_handler.decode(mock_token)

    @patch("src.core.security.jwt.settings", MagicMock(return_value=mock_settings))
    def test_decode_expired_error(self, mock_handler):
        with pytest.raises(JWTDecodeError):
            with patch.object(jwt, "decode", side_effect=JWTError):
                mock_handler.decode_expired(mock_token)
