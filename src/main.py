from presentation.urls import app
from core.settings import settings


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from infrastructure.persistence.db_session import get_db_session_manager

    db_manager = get_db_session_manager()
    is_healthy = await db_manager.health_check()

    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "database": "connected" if is_healthy else "disconnected",
        "version": settings.VERSION
    }
