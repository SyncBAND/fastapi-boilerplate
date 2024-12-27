from uuid import uuid4

from .session import local_session, reset_session_context, set_session_context


def standalone_session(func):
    async def _standalone_session(*args, **kwargs):
        session_id = str(uuid4())
        context = set_session_context(session_id=session_id)

        try:
            await func(*args, **kwargs)
        except Exception as exception:
            await local_session.rollback()
            raise exception
        finally:
            await local_session.remove()
            reset_session_context(context=context)

    return _standalone_session
