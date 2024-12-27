from typing import ClassVar, Optional

from pydantic import BaseModel, ConfigDict, Field
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class ResponseInfo(BaseModel):
    headers: Optional[Headers] = Field(default=None, json_schema_extra={"title": "Response header"})
    body: str = Field(default="", json_schema_extra={"title": "Trust"})
    status_code: Optional[int] = Field(default=None, json_schema_extra={"title": "Status code"})

    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)


class ResponseLoggerMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        response_info = ResponseInfo()

        async def _logging_send(message: Message) -> None:
            if message.get("type") == "http.response.start":
                response_info.headers = Headers(raw=message.get("headers"))
                response_info.status_code = message.get("status")
            elif message.get("type") == "http.response.body":
                if body := message.get("body"):
                    response_info.body += body.decode("utf8")

            await send(message)

        await self.app(scope, receive, _logging_send)
