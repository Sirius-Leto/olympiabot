from pydantic import BaseSettings, DirectoryPath, validator
from pathlib import Path


class Settings(BaseSettings):
    TG_TOKEN: str

    STORAGE: str = "memory"
    SUPERUSER_ID: int = 962654503
    SQLITE_URL: str = r"sqlite+aiosqlite:///db.sqlite3"

    @classmethod
    def get_project_dir(cls) -> Path:
        return Path(__file__).parent.parent


settings = Settings()
