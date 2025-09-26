from presentation.app import app
from presentation.routers import routers

app.include_router(*routers)

