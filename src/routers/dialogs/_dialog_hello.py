from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Row, Start
from aiogram_dialog.widgets.text import Const

from routers.dialogs.common_components.buttons import NAVIGATION_BAR, HELP_BUTTON
from routers.dialogs.common_components.texts import hello_message
from routers.states import MainSG, OlympiadInterestSG

ask_for_acknowledge_window = Window(
    hello_message,

    Const("\n\n"
          "Если ты знаешь, в каких олимпиадах хочешь участвовать, выбери \"Знаю в чем участвовать\" и я помогу тебе "
          "найти их. Если не знаешь, выбери \"Хочу поучаствовать, но не знаю\" и я подскажу тебе варианты. Ты также "
          "можешь обратиться за помощью, нажав на соответствующую кнопку."),
    Row(
        # SwitchTo(Const("Знаю в чем участвовать"), id="user_know_olympiad", state=MainSG.user_know_olympiad),
        Start(Const("Хочу, но не знаю"), id="user_dont_know_olympiad",
              state=OlympiadInterestSG.ask_user_for_interests),
    ),
    NAVIGATION_BAR,
    HELP_BUTTON,
    state=MainSG.start
)

dialog = Dialog(ask_for_acknowledge_window)

__all__ = ["dialog"]
