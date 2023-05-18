from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    start = State("Hello")

    class Interests(StatesGroup):
        start = State("Start")
        ask_user_for_class = State("Classes")
        ask_user_for_subjects = State("Subjects")
        ask_user_for_olympiad_level = State("Levels")

    class Help(StatesGroup):
        start = State("Help")
        faq = State("FAQ")

    class SearchOlympiads(StatesGroup):
        start = State("Search Olympiads")
        create_search_query = State("Create search query")

        class Filter(StatesGroup):
            start = State("Filter")
            subjects = State("Subjects")
            levels = State("Levels")
            types = State("Types")
            keyword = State("Keyword")

        search = State("Search")


class AdminSG(StatesGroup):
    start = State("Hello Admin")
