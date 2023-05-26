from pydantic import BaseSettings, DirectoryPath, validator
from pathlib import Path


class Settings(BaseSettings):
    TG_TOKEN: str

    STORAGE: str = "memory"
    SUPERUSER_ID: int = 962654503
    SQLITE_URL: str = r"sqlite+aiosqlite:///../db.sqlite3"
    STATIC_DIR: DirectoryPath

    @validator("STATIC_DIR", pre=True)
    def post_static_dir_validator(cls, v):
        v = Path(v)
        if not v.is_absolute():
            v = cls.get_project_dir() / v
        return v

    @classmethod
    def get_project_dir(cls) -> Path:
        return Path(__file__).parent.parent

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()

# include static dir to a python path
import sys
from pathlib import Path

sys.path.insert(0, str(Path(settings.STATIC_DIR).absolute()))
