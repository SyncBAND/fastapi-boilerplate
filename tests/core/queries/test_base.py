import pytest
import pytest_asyncio
from faker import Faker

from src.app.users.models import User
from src.core.database.session import reset_session_context, set_session_context
from src.core.queries import BaseQuery

fake = Faker()


class TestBaseQuery:
    @pytest_asyncio.fixture
    async def query(self, db_session):
        # Set session context here, e.g., setting a session ID
        context_token = set_session_context("test_session_id")
        yield BaseQuery(model=User, db_session=db_session)
        # Reset the session context after the test
        reset_session_context(context_token)

    @pytest.mark.asyncio
    async def test_create(self, query):
        user = await query.create(self._user_data_generator())
        await query.session.commit()
        assert user.id is not None

    @pytest.mark.asyncio
    async def test_get_all(self, query):
        await query.create(self._user_data_generator())
        await query.create(self._user_data_generator())
        users = await query.get_all()
        assert len(users) == 2

    def _user_data_generator(self):
        return {
            "email": fake.email(),
            "firstname": fake.first_name(),
            "lastname": fake.last_name(),
            "password": fake.password(),
        }
