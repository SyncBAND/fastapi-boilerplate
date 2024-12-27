from uuid import UUID

from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from src.app.moods.models import Mood
from src.core.database import Propagation, Transactional
from src.core.queries import BaseQuery


class MoodQuery(BaseQuery[Mood]):
    """
    Mood query provides all the database operations for the Mood model.
    """

    async def get_by_user_id(
        self, user_id: UUID, join_: set[str] | None = None
    ) -> list[Mood]:
        """
        Get all moods by user id.
        :param user_id: The user id to match.
        :param join_: The joins to make.
        :return: A list of moods.
        """
        query = self._query(join_)
        query = await self._get_by(query, "user_id", user_id)
        if join_ is not None:
            return await self._all_unique(query)
        return await self._all(query)

    @Transactional(propagation=Propagation.REQUIRED)
    async def add(self, learning: str, personal_note: str, rating: int, user_id: UUID) -> Mood:
        """
        Adds a mood.
        :param learning: The mood learning.
        :param personal_note: The mood personal_note.
        :param rating: The mood rating.
        :param user_id: The user id.
        :return: The mood.
        """
        return await self.create(
            {
                "learning": learning,
                "personal_note": personal_note,
                "rating": rating,
                "user_id": user_id,
            }
        )

    def _join_user(self, query: Select) -> Select:
        """
        Join the user relationship.
        :param query: The query to join.
        :return: The joined query.
        """
        return query.options(joinedload(Mood.user))
