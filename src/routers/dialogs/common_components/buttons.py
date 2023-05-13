from typing import Union

from aiogram_dialog import DialogManager
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Back, Next, Start, Cancel, Group, Row
from aiogram_dialog.widgets.text import Const

from ...states import HelpSG


def has_stack_above(_data: dict, _widget: Whenable, manager: DialogManager) -> bool:
    stack = manager.current_stack()
    intents = stack.intents
    return len(intents) > 1


def has_back_state(_data: dict, _widget: Whenable, manager: Union[ManagerImpl, DialogManager]) -> bool:
    context = manager.current_context()
    if not context:
        return False
    states = manager.dialog().states()
    current_index = states.index(context.state)
    return current_index > 0


def has_next_state(_data: dict, _widget: Whenable, manager: Union[ManagerImpl, DialogManager]) -> bool:
    context = manager.current_context()
    if not context:
        return False
    states = manager.dialog().states()
    current_index = states.index(context.state)
    return current_index < len(states) - 1




HELP_BUTTON = Start(Const("Помощь ❓"), id="help", state=HelpSG.help_)
BACK_BUTTON = Back(Const("Назад  ⬅️"), id="back", when=has_back_state)
NEXT_BUTTON = Next(Const("Далее  ➡️"), id="next", when=has_next_state)
EXIT_BUTTON = Cancel(Const("Выйти  🚪"), id="pop_stack", when=has_stack_above)

NAVIGATION_BAR = Group(Row(BACK_BUTTON), EXIT_BUTTON)
