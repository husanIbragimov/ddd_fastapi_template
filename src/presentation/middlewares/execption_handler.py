from fastapi.responses import JSONResponse
from application.exceptions import ExcResponse
from presentation.app import app


@app.exception_handler(ExcResponse)
def application_response_exception_handler(request, exc: ExcResponse) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "code": exc.response_code,
            "__code": exc.response_code.name if exc.response_code else None,
            "success": exc.status_code < 400 and  (exc.response_code is None or exc.response_code.is_success),
            "data": exc.data,
            "error": exc.error,
            "message": exc.message,
        },
        headers={
            "Accept-Language": request.headers.get("Accept-Language", "en"),
        }
    )