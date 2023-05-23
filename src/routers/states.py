from aiogram.fsm.state import StatesGroup, State


class UserSG(StatesGroup):
    start = State("Hello")

    class Interests(StatesGroup):
        start = State("Start")
        ask_grades = State("Grades")
        ask_subjects = State("Subjects")
        ask_levels = State("Levels")

    class Help(StatesGroup):
        start = State("Help")
        faq = State("FAQ")

    class SearchOlympiads(StatesGroup):
        start = State("Search Olympiads")

        filters = State("Filter")

        filter_name = State("Name")
        filter_subjects = State("Subjects")
        filter_levels = State("Levels")
        filter_grades = State("Grades")
        filter_by_date = State("Date")
        # filter_types = State("Types")

        list_olympiads = State("List Olympiads")
        show_olympiad = State("Show Olympiad")


class AdminSG(StatesGroup):
    start = State("Hello Admin")
