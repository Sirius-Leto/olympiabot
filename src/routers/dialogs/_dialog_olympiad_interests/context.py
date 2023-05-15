from collections import defaultdict
from typing import Any

from utilities import SingletonMeta


class OptionsSingleton(metaclass=SingletonMeta):
    classes_options: list[tuple[str, str]]
    subjects_options: list[tuple[str, str]]
    levels_options: list[tuple[str, str]]

    def __init__(self, **kwargs):
        self.classes_options = kwargs.get("classes_options", [
            ("👶 1-5 класс", (1, 2, 3, 4, 5)),
            ("🧑‍🎓 6-8 класс", (6, 7, 8)),
            ("👨‍🎓 9-11 класс", (9, 10, 11)),
        ])

        self.subjects_options = kwargs.get("subjects_options", [
            ("🔢 Математика", "math"),
            ("📚 Русский язык", "russian"),
            ("💻 Информатика", "informatics"),
            ("🔬 Физика", "physics"),
            ("🧪 Химия", "chemistry"),
            ("🧬 Биология", "biology"),
            ("🌍 География", "geography"),
            ("⏳ История", "history"),
            ("👥 Обществознание", "social_science"),
            ("🖋️ Литература", "literature"),
            ("🌐 Иностранный язык", "foreign_language")
        ])

        self.levels_options = kwargs.get("levels_options", [
            ("🏅 Перечень РСОШ 1 уровня", "RCSO1"),
            ("🥈 Перечень РСОШ 2 уровня", "RCSO2"),
            ("🥉 Перечень РСОШ 3 уровня", "RCSO3"),
            ("🇷🇺 Всероссийская олимпиада", "all_russia"),
            ("🌍 Международная олимпиада", "international")
        ])

    def get_options(self) -> dict[str, list[tuple[str, str]]]:
        return {
            "classes_options": self.classes_options,
            "subjects_options": self.subjects_options,
            "levels_options": self.levels_options
        }


class InterestContext:
    """Контекст для диалога выбора интересов пользователя. Принадлежит конкретному пользователю."""
    __options: OptionsSingleton
    __chosen: defaultdict[str, set[Any]]

    def __init__(self):
        self.__options = OptionsSingleton()
        self.__chosen = defaultdict(set)

    def get_options(self) -> dict[str, list[tuple[str, Any]]]:
        return self.__options.get_options()

    def get_chosen(self, key: str) -> set:
        return self.__chosen[key].copy()

    def get_result(self) -> dict[str, set[Any]]:
        return dict(self.__chosen)

    def add_chosen(self, key: str, value: Any):
        self.__chosen[key].add(value)

    def remove_chosen(self, key: str, value: Any):
        self.__chosen[key].remove(value)
