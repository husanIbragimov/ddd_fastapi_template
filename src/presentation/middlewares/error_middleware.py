from fastapi import Request
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse


async def validation_error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except ResponseValidationError as exc:
        print("Validation Error Middleware Triggered")
        print(exc)
        print(exc.body)
        print(exc.errors())
        return JSONResponse(
            status_code=422,
            content=exc.body
        )
