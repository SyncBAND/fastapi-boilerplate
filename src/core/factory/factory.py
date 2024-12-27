from functools import partial

from fastapi import Depends

from src.app.auth.queries import AuthQuery
from src.app.moods.models import Mood
from src.app.moods.queries import MoodQuery
from src.app.users.models import User
from src.app.users.queries import UserQuery
from src.core.database import async_get_session


class Factory:
    """
    Factory container that instantiates all queries which can be accessed 
    by the rest of the application.
    """
    # Queries with their respective models
    auth_query = partial(AuthQuery, User)
    mood_query = partial(MoodQuery, Mood)
    user_query = partial(UserQuery, User)

    def get_auth_query(self, db_session=Depends(async_get_session)):
        """
        Returns a query instance for authentication.
        """
        return self.auth_query(db_session=db_session)

    def get_mood_query(self, db_session=Depends(async_get_session)):
        """
        Returns a mood query instance.
        """
        return self.mood_query(db_session=db_session)

    def get_user_query(self, db_session=Depends(async_get_session)):
        """
        Returns a user query instance.
        """
        return self.user_query(db_session=db_session)
