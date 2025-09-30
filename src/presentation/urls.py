from presentation.app import app
from presentation.routers import routers

for router in routers:
    app.include_router(router)
