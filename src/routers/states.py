from aiogram.fsm.state import StatesGroup, State


class MainSG(StatesGroup):
    start = State("Start")
    user_know_olympiad = State("UserKnowOlympiad", group_name="ask_for_acknowledge")
    user_dont_know_olympiad = State("UserDontKnowOlympiad", group_name="ask_for_acknowledge")


class HelpSG(StatesGroup):
    help_ = State("Help")
    faq = State("FAQ")


class AdminSG(StatesGroup):
    admin_panel = State("AdminPanel")
