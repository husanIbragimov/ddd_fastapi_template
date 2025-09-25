from fastapi import HTTPException

from core.response.response_code import ResponseCode


class ExceptionResponse(HTTPException):
    def __init__(self, status_code, response_code: ResponseCode | None, detail=None, data=None):
        data = {
            "status": status_code,
            "is_success": status_code < 400,
            "code_detail": response_code.name if response_code else None,
            "response_code": response_code.value if response_code else None,
            "error": detail,
            "data": data,
        }
        super().__init__(status_code=status_code, detail=data)
        self.detail = data
        self.status_code = status_code
