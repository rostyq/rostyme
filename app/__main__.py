from uvicorn import run
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 5000

    reload: bool = False
    debug: bool = False
    workers: int = 1


settings = Settings()

if settings.reload and not settings.debug:
    app = "app:app"
else:
    from app import app

    app.debug = settings.debug

run(app,
    reload=settings.reload,
    port=settings.port,
    host=settings.host,
    workers=settings.workers)
