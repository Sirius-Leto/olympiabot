# from src.data.storages.sqldatabase import SQLiteStorage
# from src.config import settings

import datetime
from typing import Optional

from pydantic import BaseModel, validator
import re


# {
#       "name": "Олимпиада школьников «Ломоносов» по психологии",
#       "begin-date": "27-11-2023",
#       "end-date": "11-03-2024",
#       "type": "олимпиада",
#       "level": 1,
#       "format": "Нужно пройти дистанционный отбор, чтобы участвовать в очном финале",
#       "grade": "5–11 классы",
#       "subjects": [
#         "Биология",
#         "Психология"
#       ],
#       "prizes": "Nothing found",
#       "URL": "https://olimpiada.ru//activity/328"
#     }
class Entry(BaseModel):
    name: str
    begin_date: datetime.date  # in file: begin-date and dd-mm-yyyy
    end_date: datetime.date  # in file: end-date and dd-mm-yyyy
    event_type: str
    level: int
    format: Optional[str]
    grade: list[int]
    subjects: list[str]
    prizes: Optional[str]
    url: str

    class Config:
        fields = {
            "begin_date": "begin-date",
            "end_date": "end-date",
            "url": "URL",
            "event_type": "type"
        }

    @validator("begin_date", "end_date", pre=True)
    def parse_date(cls, v):
        return datetime.datetime.strptime(v, "%d-%m-%Y").date()

    @validator("grade", pre=True)
    def parse_grade(cls, v):
        # "5–11 классы" -> ["5", "6", "7", "8", "9", "10", "11"]
        v = re.sub(r"–", "-", v)
        v = re.sub(r"класс(ы)?", "", v)
        v = v.strip()
        left, right = v.split("-")
        return [i for i in range(int(left), int(right) + 1)]

    @validator("format", "prizes", pre=True)
    def delete_not_found(cls, v):
        if "Nothing found" in v:
            return None


# async def main():
#     storage = SQLiteStorage.from_url(settings.database_url)
#     await storage.create_all()


import json

if __name__ == '__main__':
    path_to_json = r"C:\Users\dante\PycharmProjects\sirius-olympiad\src\static\parsed.json"

    with open(path_to_json, "r", encoding="utf-8") as read_file:
        data = json.load(read_file)

    entries = []
    for entry in data["instances"]:
        entries.append(Entry(**entry))

    print(entries[0])
