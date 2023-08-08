from pydantic_settings import BaseSettings, SettingsConfigDict


__all__ = ["settings"]


class Settings(BaseSettings):
    base_url: str

    host: str = "localhost"
    port: int = 5000
    reload: bool = False
    debug: bool = False
    workers: int = 1

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
