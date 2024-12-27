import pytest
from httpx import AsyncClient

from tests.factory.users import create_fake_user
from tests.utils.login import _create_user_and_login

REGISTER_URL = "/api/register"
LOGIN_URL = "/api/login"
USERS_URL = "/api/users"


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient) -> None:
    """Test user creation."""
    fake_user = create_fake_user()
    response = await client.post(REGISTER_URL, json=fake_user)
    assert response.status_code == 201
    assert response.json()["email"] == fake_user["email"]
    assert response.json()["firstname"] == fake_user["firstname"]
    assert response.json()["lastname"] == fake_user["lastname"]


@pytest.mark.asyncio
async def test_create_user_with_existing_email(client: AsyncClient) -> None:
    """Test user creation with existing email."""
    fake_user = create_fake_user()

    await client.post(REGISTER_URL, json=fake_user)

    response = await client.post(REGISTER_URL, json=fake_user)
    assert response.status_code == 400
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_create_user_with_invalid_email(client: AsyncClient) -> None:
    """Test user creation with invalid email."""
    fake_user = create_fake_user()
    fake_user["email"] = "invalid_email"

    response = await client.post(REGISTER_URL, json=fake_user)
    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_create_user_with_invalid_firstname(client: AsyncClient) -> None:
    """Test user creation with invalid firstname."""
    fake_user = create_fake_user()
    fake_user["firstname"] = "<invalid_firstname>"

    response = await client.post(REGISTER_URL, json=fake_user)
    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_create_user_with_invalid_password(client: AsyncClient) -> None:
    """Test user creation with invalid password."""
    fake_user = create_fake_user()
    fake_user["password"] = "123"

    response = await client.post(REGISTER_URL, json=fake_user)
    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_user_login(client: AsyncClient) -> None:
    """Test user login."""
    fake_user = create_fake_user()

    await client.post(REGISTER_URL, json=fake_user)

    response = await client.post(LOGIN_URL, json=fake_user)
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["refresh_token"] is not None


@pytest.mark.asyncio
async def test_user_login_with_invalid_email(client: AsyncClient) -> None:
    """Test user login with invalid email."""
    fake_user = create_fake_user()
    fake_user["email"] = "invalid_email"

    response = await client.post(LOGIN_URL, json=fake_user)
    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_user_login_with_invalid_password(client: AsyncClient) -> None:
    """Test user login with invalid password."""
    fake_user = create_fake_user()
    fake_user["password"] = "1"

    response = await client.post(LOGIN_URL, json=fake_user)
    assert response.status_code == 400
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_get_all_users(client: AsyncClient) -> None:
    """Test get all users."""

    await _create_user_and_login(client)

    response = await client.get(USERS_URL)
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["email"] is not None


@pytest.mark.asyncio
async def test_unauthorized_get_all_users(client: AsyncClient) -> None:
    """Test get all users."""

    # Clear headers
    client.headers.clear()

    response = await client.get(USERS_URL)
    assert response.status_code == 401
    assert response.json() is not None


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient) -> None:
    """Test get me."""
    fake_user = create_fake_user()

    await _create_user_and_login(client, fake_user)

    response = await client.get(f"{USERS_URL}/me")
    assert response.status_code == 200
    assert response.json()["email"] == fake_user["email"]
    assert response.json()["firstname"] == fake_user["firstname"]
