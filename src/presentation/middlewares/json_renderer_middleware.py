import json

from fastapi import Request
from starlette.middleware.base import _StreamingResponse
from starlette.responses import Response

async def json_renderer_middleware(request: Request, call_next) -> Response:
    response: _StreamingResponse = await call_next(request)
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    # Faqat JSON bo'lsa va bo'sh bo'lmasa ishlash
    if response_body and response.media_type == "application/json":
        try:
            response_json = json.loads(response_body.decode("utf-8"))
            response_json["new_field"] = "new data"
            modified_response = json.dumps(response_json).encode("utf-8")
            response.headers['Content-Length'] = str(len(modified_response))
            return Response(
                content=modified_response,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
        except json.JSONDecodeError:
            pass  # JSON emas yoki noto'g'ri format

    # Aks holda asl javobni qaytarish
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )
