from typing import Callable
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status
from pydantic import UUID4

from src.app.moods.models import MoodPermission
from src.app.moods.queries import MoodQuery
from src.app.moods.schemas import MoodSchema, MoodDetailSchema
from src.core.factory import Factory
from src.core.dependencies.permissions import Permissions


mood_router = APIRouter(tags=["Moods"])


@mood_router.get("/", response_model=list[MoodDetailSchema])
async def get_moods(
    request: Request,
    mood_query: MoodQuery = Depends(Factory().get_mood_query),
    assert_access: Callable = Depends(Permissions(MoodPermission.READ))
) -> list[MoodDetailSchema]:
    moods = await mood_query.get_by_user_id(request.user.id)
    assert_access(moods)
    return moods


@mood_router.post("/", response_model=MoodDetailSchema, status_code=status.HTTP_201_CREATED)
async def create_mood(
    request: Request,
    mood_create: MoodSchema,
    mood_query: MoodQuery = Depends(Factory().get_mood_query)
) -> MoodDetailSchema:
    mood = await mood_query.add(
        learning=mood_create.learning,
        personal_note=mood_create.personal_note,
        rating=mood_create.rating,
        user_id=request.user.id,
    )
    await mood_query.session.flush()
    return mood


@mood_router.get("/{mood_id}", response_model=MoodDetailSchema)
async def get_mood(
    mood_id: UUID4,
    mood_query: MoodQuery = Depends(Factory().get_mood_query),
    assert_access: Callable = Depends(Permissions(MoodPermission.READ)),
) -> MoodDetailSchema:
    mood = await mood_query.get_by_id(mood_id)
    assert_access(mood)
    return mood


@mood_router.put("/{mood_id}", response_model=MoodDetailSchema)
async def update_mood(
    mood_id: UUID,
    mood_update: MoodSchema,
    mood_query: MoodQuery = Depends(Factory().get_mood_query),
    assert_access: Callable = Depends(Permissions(MoodPermission.EDIT)),
) -> MoodDetailSchema:
    mood = await mood_query.get_by_id(mood_id)
    assert_access(mood)
    # Update logic here
    return mood


@mood_router.delete("/{mood_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mood(
    mood_id: UUID,
    mood_query: MoodQuery = Depends(Factory().get_mood_query),
    assert_access: Callable = Depends(Permissions(MoodPermission.DELETE)),
) -> None:
    mood = await mood_query.get_by_id(mood_id)
    assert_access(mood)
    mood_query.delete(mood_id)
