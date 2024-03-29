# from src.data.storages.sqldatabase import SQLiteStorage
# from src.config import settings

import datetime
import json
import operator
import re
from collections import defaultdict
from typing import Optional

from pydantic import BaseModel, validator, ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from data.models import *
from data.storages.sqldatabase import SQLiteStorage


# {
#         "name": "Олимпиада «Газпром»",
#         "description": "«Газпром» совместно с ведущими техническими и экономическими вузами России проводит отраслевую олимпиаду для учеников 9-11 классов по математике, физике, химии, информатике, инженерному делу и экономике. Соревнования проходят в два этапа: отборочный (дистанционный) и заключительный (очный). К участию в финале допускаются победители и призеры отборочного этапа. Каждый вуз-организатор является также площадкой для написания очного этапа.  ",
#         "begin_date": "10-10-2023",
#         "end_date": "12-03-2024",
#         "event_type": "олимпиада",
#         "level": 2,
#         "format": "Очно-заочная. Нужно пройти дистанционный отбор, чтобы участвовать в очном финале",
#         "grade": [
#             9,
#             10,
#             11
#         ],
#         "subjects": [
#             "Информатика",
#             "Математика",
#             "Физика",
#             "Химия",
#             "Экономика"
#         ],
#         "prizes": "Nothing found",
#         "URL": "https://olimpiada.ru/activity/5516"
#     }

class Entry(BaseModel):
    name: str
    description: Optional[str]
    begin_date: Optional[datetime.datetime]  # in file: begin-date and dd-mm-yyyy
    end_date: Optional[datetime.datetime]  # in file: end-date and dd-mm-yyyy
    event_type: str
    level: str
    format: Optional[str]
    grade: list[str]
    subjects: list[str]
    prizes: Optional[str]
    url: str

    class Config:
        fields = {
            "begin_date": "begin-date",
            "end_date": "end-date",
            "url": "URL",
        }

    @validator("begin_date", "end_date", pre=True)
    def parse_date(cls, v):
        if v is None:
            return None
        return datetime.datetime.strptime(v, "%d-%m-%Y")

    @validator("grade", pre=True)
    def parse_grade(cls, v):
        return list(map(str, v))

    @validator("format", "prizes", pre=True)
    def delete_not_found(cls, v):
        if "Nothing found" in v:
            return None
        return v


async def get_or_create(session: AsyncSession, model: type, **kwargs):
    instance = await session.scalar(select(model).filter_by(**kwargs))
    if instance is None:
        instance = model(**kwargs)
        session.add(instance)
    return instance


TAGS = [
    # ("Олимпиада «Газпром»", "https://olympiad.gazprom.ru/"),
    # ("Олимпиада «Высшая проба»", "https://olymp.hse.ru/mmo/"),
    # ("Всесибирская открытая олимпиада школьников", "https://sesc.nsu.ru/olymp-vsesib/"),
    # ("Олимпиада школьников «Физтех»", "https://olymp.mipt.ru/"),
    # ("Олимпиада «Юные таланты»", "http://olymp.psu.ru/"),
    # ("Олимпиада школьников «Ломоносов»", "https://olymp.msu.ru/"),
    # ("Олимпиада СПбГУ", "https://olympiada.spbu.ru/"),
    # ("Олимпиада «Покори Воробьевы горы!»", "https://pvg.mk.ru/"),
    # ("Всероссийская олимпиада", "https://vserosolimp.edsoo.ru/"),
    ("Национальная технологическая олимпиада (НТО)", "https://ntcontest.ru/"),
]

LEVELS = [
    ("0", "Всероссийская олимпиада"),
    ("1", "Перечень РСОШ 1 уровня"),
    ("2", "Перечень РСОШ 2 уровня"),
    ("3", "Перечень РСОШ 3 уровня"),
]

FOREIGN_LANGUAGES = [
    "Китайский",
    "Французский",
    "Испанский",
    "Немецкий",
    "Японский",
    "Английский",
    "Арабский",
    "Португальский",
    "Русский",
    "Итальянский",
    "Корейский",
    "Турецкий",
    "Польский",
]


async def main():
    storage = SQLiteStorage.from_url(settings.SQLITE_URL)
    await storage.create_all()

    path_to_json = r"C:\Users\dante\PycharmProjects\sirius-olympiad\src\static\nto.json"

    with open(path_to_json, "r", encoding="utf-8") as read_file:
        data = json.load(read_file)

    entries = []

    for entry in data:
        entries.append(Entry(**entry))

    unique_values = defaultdict(set)

    unique_values["tags"] = set(TAGS)

    for entry in entries:
        unique_values["event_type"].add(entry.event_type)
        unique_values["grade"].update(entry.grade)
        unique_values["subjects"].update(entry.subjects)
        # unique_values["format"].add(entry.format)
        # unique_values["prizes"].add(entry.prizes)

    async with storage.create_session() as session:
        for event_type in unique_values["event_type"]:
            await get_or_create(session, EventTypeModel, name=event_type)

        for level_name, level_desc in LEVELS:
            await get_or_create(session, LevelModel, name=level_name, description=level_desc)

        for grade in unique_values["grade"]:
            await get_or_create(session, GradeModel, name=grade)

        for subject in unique_values["subjects"]:
            await get_or_create(session, SubjectModel, name=subject)

        # add subjects for foreign languages
        foreign_languages_subject = await get_or_create(session, SubjectModel, name="Иностранный язык")

        for tag_name, tag_desc in unique_values["tags"]:
            await get_or_create(session, TagModel, name=tag_name, description=tag_desc)

        nto_tag = select(TagModel).filter_by(name="Национальная технологическая олимпиада (НТО)")
        nto_tag = await session.scalar(nto_tag)

        # check on foreign language

        tag_names = set(map(operator.itemgetter(0), unique_values["tags"]))
        events = []

        for entry in entries:
            # get event if exist continue else create
            event = await session.scalar(select(EventModel).filter_by(name=entry.name))
            print(event)
            if event is not None:
                continue

            event_type = await session.scalar(select(EventTypeModel).filter_by(name=entry.event_type))
            levels = [await session.scalar(select(LevelModel).filter_by(name=entry.level))]
            grades = await session.scalars(select(GradeModel).filter(GradeModel.name.in_(entry.grade)))
            subjects = await session.scalars(select(SubjectModel).filter(SubjectModel.name.in_(entry.subjects)))

            event = EventModel(
                name=entry.name,
                description=entry.description,
                begin_date=entry.begin_date,
                end_date=entry.end_date,
                url=entry.url,
                format=entry.format,
                prizes=entry.prizes,
                event_type=event_type,
                levels=levels,
                grades=grades.all(),
                subjects=subjects.all(),
            )

            # # if some tag name in event name
            # for tag_name in tag_names:
            #     if tag_name in entry.name:
            #         tag = await session.scalar(select(TagModel).filter_by(name=tag_name))
            #         event.tags.append(tag)

            event.tags.append(nto_tag)

            # if some foreign language in event name
            for foreign_language in FOREIGN_LANGUAGES:
                if foreign_language in entry.subjects:
                    event.subjects.append(foreign_languages_subject)
                    break

            events.append(event)

        session.add_all(events)
        await session.commit()


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
