from presentation.app import app
from presentation.handlers.auth import auth_router

app.include_router(auth_router)


@app.get("/app", response_model=dict, tags=["app"])
def main():
    return {
        "message": "FastAPI is running!",
    }
