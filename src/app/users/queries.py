from uuid import UUID

from sqlalchemy import Select
from sqlalchemy.orm import joinedload

from src.app.users.models import User
from src.core.queries import BaseQuery


RELATIONSHIPS = {"moods"}


class UserQuery(BaseQuery[User]):
    """
    User query provides all the database operations for the User model.
    """

    async def get_all(self, skip: int = 0, limit: int = 100, join_: set[str] | None = None):
        if join_ is None:
            join_ = RELATIONSHIPS
        return await super().get_all(skip=skip, limit=limit, join_=join_)

    async def get_by_id(self, id_: UUID, join_: set[str] | None = None):
        if join_ is None:
            join_ = RELATIONSHIPS
        return await super().get_by_id(id_=id_, join_=join_)

    async def get_by_email(self, email: str, join_: set[str] | None = None) -> User | None:
        """
        Get user by email.
        :param email: Email.
        :param join_: Join relations.
        :return: User.
        """
        query = self._query(join_)
        query = query.filter(User.email == email)
        if join_ is not None:
            return await self._all_unique(query)
        return await self._one_or_none(query)

    def _join_moods(self, query: Select) -> Select:
        """
        Join tasks.
        :param query: Query.
        :return: Query.
        """
        return query.options(joinedload(User.moods)).execution_options(
            contains_joined_collection=True
        )
