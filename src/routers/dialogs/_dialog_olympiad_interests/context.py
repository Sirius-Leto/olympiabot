from collections import defaultdict
from typing import Any, Union

from ..common_components.emojis import SUBJECTS_EMOJIS, DEFAULT_SUBJECT_EMOJI
from utilities import SingletonMeta


class InterestOptionsSingleton(metaclass=SingletonMeta):
    grades_options: list[tuple[str, str]]
    subjects_options: list[tuple[str, str]]
    levels_options: list[tuple[str, str]]

    def __init__(self) -> None:
        self.grades_options = [
            ("👶 9 класс", "9"),
            ("🧑‍ 10 класс", "10"),
            ("👨‍🎓 11 класс", "11"),
        ]
        subject_names = (
            "Математика",
            "Русский",
            "Информатика",
            "Физика",
            "Химия",
            "Биология",
            "География",
            "История",
            "Обществознание",
            "Литература",
            "Иностранный язык",
        )

        self.subjects_options = [
            (f"{SUBJECTS_EMOJIS.get(subject_name, DEFAULT_SUBJECT_EMOJI)} {subject_name}", subject_name)
            for subject_name in subject_names]

        self.levels_options = [
            ("🇷🇺 Всероссийская олимпиада", "0"),
            ("🏅 Перечень РСОШ 1 уровня", "1"),
            ("🥈 Перечень РСОШ 2 уровня", "2"),
            ("🥉 Перечень РСОШ 3 уровня", "3"),
            # ("🌍 Международная олимпиада", "international")
        ]

    def get_options(self) -> dict[str, list[tuple[str, Any]]]:
        return {
            "grades_options": self.grades_options,
            "subjects_options": self.subjects_options,
            "levels_options": self.levels_options
        }


class InterestContext:
    """Контекст для диалога выбора интересов пользователя. Принадлежит конкретному пользователю."""
    __options: InterestOptionsSingleton
    __chosen: defaultdict[str, set[Any]]

    def __init__(self, options: InterestOptionsSingleton) -> None:
        self.__options = options
        self.__chosen = defaultdict(set)

    def get_options(self) -> dict[str, list[tuple[str, Any]]]:
        return self.__options.get_options()

    def get_chosen(self, key: str) -> set:
        return self.__chosen[key].copy()

    def get_result(self) -> dict[str, set]:
        result = dict(self.__chosen)

        if "grades" in result:
            _ = []
            for grade in result["grades"]:
                _.extend(grade.split())
            result["grades"] = set(_)

        return result

    def add_chosen(self, key: str, value: Any):
        self.__chosen[key].add(value)

    def set_chosen(self, key: str, value: Union[set, list, tuple]):
        self.__chosen[key] = set(value)

    def remove_chosen(self, key: str, value: Any):
        self.__chosen[key].discard(value)
