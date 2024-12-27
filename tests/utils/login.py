from httpx import AsyncClient

from tests.factory.users import create_fake_user


async def _create_user_and_login(client: AsyncClient, fake_user=None):
    """
    Create a user and log them in.
    
    Args:
        client: The test client
        fake_user: Optional user data dictionary. If None, generates new fake data.
    """
    if fake_user is None:
        fake_user = create_fake_user()

    await client.post("/api/register", json=fake_user)
    response = await client.post("/api/login", json=fake_user)

    access_token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {access_token}"})


__all__ = ["_create_user_and_login"]
