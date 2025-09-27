from presentation.urls import app


@app.get("/", status_code=200)
async def root() -> dict:
    return {"message": "Welcome to FastAPI Application!"}
