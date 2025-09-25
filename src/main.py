from presentation.app import app



@app.get("/app", response_model=dict, tags=["app"])
def main():
    return {
        "message": "FastAPI is running!",
    }
