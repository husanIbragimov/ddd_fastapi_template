from typing import Any

from .response_code import ResponseCode


class ExcResponse(Exception):

    def __init__(self,
                 status_code: int,
                 response_code: ResponseCode | None = None,
                 message : dict[str, str] | None = None,
                 data: dict[str, Any] | None = None,
                 error: str | None = None
    ):
        self.status_code = status_code
        self.response_code = response_code
        self.message = message
        self.error = error
        self.data = data