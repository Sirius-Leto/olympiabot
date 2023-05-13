from pydantic import BaseSettings


class Settings(BaseSettings):
    TG_TOKEN: str

    STORAGE: str = "memory"
    SUPERUSER_ID: int = 962654503
    SQLITE_URL: str = "sqlite+aiosqlite:///db.sqlite3"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
