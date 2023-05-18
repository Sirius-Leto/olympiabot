from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo, Group, Column, Multiselect, Button, Cancel, Start
from aiogram_dialog.widgets.text import Const, Format

from routers.dialogs.common_components.buttons import NAVIGATION_BAR, EXIT_OR_START_BUTTON, HELP_BUTTON
from routers.states import MainSG

start_window = Window(
    Const(
        "Для поиска олимпиад, пожалуйста, укажи критерии поиска. Ты можешь выбрать предмет, уровень, тип олимпиады "
        "или указать ключевое слово. Если нужна помощь, нажми \"Помощь\"."
    ),
    Start(Const("Указать критерии поиска"), id="start_searching_olympiads", state=MainSG.SearchOlympiads.Filter.start),
    HELP_BUTTON,
    state=MainSG.SearchOlympiads.start
)

windows = []

dialog = Dialog(*windows)

__all__ = ["dialog"]
