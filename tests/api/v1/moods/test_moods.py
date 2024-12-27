import pytest
from httpx import AsyncClient

from tests.factory.moods import create_fake_mood
from tests.utils.login import _create_user_and_login


@pytest.mark.asyncio
async def test_create_mood(client: AsyncClient, db_session) -> None:
    """Test mood creation."""
    await _create_user_and_login(client)

    fake_mood = create_fake_mood()
    response = await client.post("/api/moods/", json=fake_mood)
    assert response.status_code == 201
    assert response.json()["learning"] == fake_mood["learning"]
    assert response.json()["personal_note"] == fake_mood["personal_note"]
    assert response.json()["rating"] == fake_mood["rating"]


@pytest.mark.asyncio
async def test_create_mood_with_invalid_learning(client: AsyncClient, db_session) -> None:
    """Test mood creation with invalid learning."""
    await _create_user_and_login(client)

    fake_mood = create_fake_mood()
    fake_mood["learning"] = ""

    response = await client.post("/api/moods/", json=fake_mood)
    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_create_mood_with_invalid_personal_note(
    client: AsyncClient, db_session
) -> None:
    """Test mood creation with invalid personal_note."""
    await _create_user_and_login(client)

    fake_mood = create_fake_mood()
    fake_mood["personal_note"] = ""

    response = await client.post("/api/moods/", json=fake_mood)
    assert response.status_code == 422
    assert response.json()["detail"] is not None


@pytest.mark.asyncio
async def test_get_all_moods(client: AsyncClient, db_session) -> None:
    """Test get all moods."""
    await _create_user_and_login(client)

    await client.post("/api/moods/", json=create_fake_mood())
    await client.post("/api/moods/", json=create_fake_mood())
    await client.post("/api/moods/", json=create_fake_mood())

    response = await client.get("/api/moods/")
    assert response.status_code == 200
    assert len(response.json()) == 3
