from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const

from routers.dialogs.common_components.buttons import NAVIGATION_BAR, HELP_BUTTON
from routers.dialogs.common_components.texts import hello_message
from routers.states import UserSG

ask_for_acknowledge_window = Window(
    hello_message,

    Const("\n\n"
          "Если ты знаешь, в каких олимпиадах хочешь участвовать, выбери \"Знаю в чем участвовать\" и я помогу тебе "
          "найти их. Если не знаешь, выбери \"Хочу поучаствовать, но не знаю\" и я подскажу тебе варианты. Ты также "
          "можешь обратиться за помощью, нажав на соответствующую кнопку."),
    Row(
        Start(Const("Хочу, но не знаю"), id="user_dont_know_olympiad", state=UserSG.Interests.start),
        Start(Const("Знаю, в чём участвовать"), id="user_know_olympiad", state=UserSG.SearchOlympiads.start)
    ),
    NAVIGATION_BAR,
    HELP_BUTTON,
    state=UserSG.start
)

windows = [ask_for_acknowledge_window]
dialog = Dialog(*windows)

__all__ = ["dialog"]
