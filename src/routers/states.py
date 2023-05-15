from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    start = State("Start")


class OlympiadInterestSG(StatesGroup):
    ask_user_for_interests = State("AskUserForInterests")
    ask_user_for_class = State("AskUserForClass")
    ask_user_for_subjects = State("AskUserForSubjects")
    ask_user_for_olympiad_level = State("AskUserForOlympiadLevel")


class HelpSG(StatesGroup):
    help_ = State("Help")
    faq = State("FAQ")


class AdminSG(StatesGroup):
    admin_panel = State("AdminPanel")
