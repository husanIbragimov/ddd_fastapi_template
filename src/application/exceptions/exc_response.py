from typing import Any

from fastapi import HTTPException

from .response_code import ResponseCode


class ExcResponse(HTTPException):

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

        super().__init__(status_code=status_code, detail=self._build_response())

    def _build_response(self) -> dict[str, Any]:
        response = {}
        if self.response_code is not None:
            response["code"] = self.response_code.value
        if self.message is not None:
            response["message"] = self.message
        if self.error is not None:
            response["error"] = self.error
        if self.data is not None:
            response["data"] = self.data
        return response
