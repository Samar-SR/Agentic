from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    Gorq_API : str

    model_config = SettingsConfigDict(env_file=(".env","../.env"), env_file_encoding="utf-8")

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()







