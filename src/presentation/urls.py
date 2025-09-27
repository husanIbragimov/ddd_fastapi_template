from presentation.app import app
from presentation.routers import routers

for router in routers:
    print(router, "included")
    app.include_router(router)
