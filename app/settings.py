from os import getenv

from pydantic import Field
from pydantic_settings import BaseSettings


__all__ = ["settings"]


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 5000


def get_default_base_url() -> str:
    host = getenv('HOST', DEFAULT_HOST)
    port = getenv('PORT', DEFAULT_PORT)
    return f"http://{host}:{port}"


class Settings(BaseSettings):
    host: str = DEFAULT_HOST
    port: int = DEFAULT_PORT

    base_url: str = Field(default_factory=get_default_base_url)

    reload: bool = False
    debug: bool = False
    workers: int = 1

    production: bool = False

    allowed_hosts: list[str] = ["*"]

settings = Settings()
