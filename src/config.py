from pydantic import BaseSettings


class Settings(BaseSettings):
    TG_TOKEN: str

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = "redis"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
