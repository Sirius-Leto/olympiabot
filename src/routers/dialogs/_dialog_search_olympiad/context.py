from collections import defaultdict
from typing import Any, Union

from routers.dialogs.common_components.emojis import SUBJECTS_EMOJIS, DEFAULT_SUBJECT_EMOJI
from utilities import SingletonMeta

from data.repositories.olympiads import AbstractOlympiadsRepository
from data.schemas import EventView


class FilterOptionsSingleton(metaclass=SingletonMeta):
    grades_options: list[tuple[str, str]]
    subjects_options: list[tuple[str, str]]
    levels_options: list[tuple[str, str]]

    olympiad_repository: AbstractOlympiadsRepository

    def __init__(self, olympiad_repository: AbstractOlympiadsRepository) -> None:
        self.olympiad_repository = olympiad_repository

    async def init(self) -> None:
        self.grades_options = [
            ("👶 1 класс", "1"),
            ("👶 2 класс", "2"),
            ("👶 3 класс", "3"),
            ("👶 4 класс", "4"),
            ("👶 5 класс", "5"),

            ("🧑‍ 6 класс", "6"),
            ("🧑‍ 7 класс", "7"),
            ("🧑‍ 8 класс", "8"),

            ("👨‍🎓 9 класс", "9"),
            ("👨‍🎓 10 класс", "10"),
            ("👨‍🎓 11 класс", "11"),
        ]

        subjects = await self.olympiad_repository.get_all_subjects()
        grades = await self.olympiad_repository.get_all_grades()

        subject_names = [subject.name for subject in subjects]
        subject_names.sort()

        self.subjects_options = [
            (f"{SUBJECTS_EMOJIS.get(subject_name, DEFAULT_SUBJECT_EMOJI)}  {subject_name}", subject_name)
            for subject_name in subject_names]

        self.levels_options = [
            ("🏅 Перечень РСОШ 1 уровня", "1"),
            ("🥈 Перечень РСОШ 2 уровня", "2"),
            ("🥉 Перечень РСОШ 3 уровня", "3"),
            ("🇷🇺 Всероссийская олимпиада", "0"),
            # ("🌍 Международная олимпиада", "international")
        ]

    def get_options(self) -> dict[str, list[tuple[str, Any]]]:
        return {
            "grades_options": self.grades_options,
            "subjects_options": self.subjects_options,
            "levels_options": self.levels_options
        }


class FilterContext:
    """Контекст для диалога выбора интересов пользователя. Принадлежит конкретному пользователю."""
    __options: FilterOptionsSingleton
    __chosen: defaultdict[str, set[Any]]

    filtered_olympiads: list[EventView]
    chosen_olympiad: EventView

    def __init__(self, options: FilterOptionsSingleton) -> None:
        self.__options = options
        self.__chosen = defaultdict(set)
        self.filtered_olympiads = []

    def get_options(self) -> dict[str, list[tuple[str, Any]]]:
        return self.__options.get_options()

    def get_chosen(self, key: str) -> set:
        return self.__chosen[key].copy()

    def get_result(self) -> dict[str, set]:
        result = dict(self.__chosen)
        return result

    def add_chosen(self, key: str, value: Any):
        self.__chosen[key].add(value)

    def set_chosen(self, key: str, value: Union[set, list, tuple]):
        self.__chosen[key] = set(value)

    def remove_chosen(self, key: str, value: Any):
        self.__chosen[key].discard(value)
