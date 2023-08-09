from uvicorn import run
from .settings import settings


if settings.reload or settings.workers > 1 and not settings.debug:
    app = "app:app"
else:
    from app import app

run(app,
    reload=settings.reload,
    port=settings.port,
    host=settings.host,
    workers=settings.workers)
