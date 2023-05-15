from pydantic import BaseSettings, DirectoryPath


class Settings(BaseSettings):
    TG_TOKEN: str

    STORAGE: str = "memory"
    SUPERUSER_ID: int = 962654503
    SQLITE_URL: str = "sqlite+aiosqlite:///db.sqlite3"
    STATIC_DIR: DirectoryPath

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()

# include static dir to a python path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(settings.STATIC_DIR).absolute()))
