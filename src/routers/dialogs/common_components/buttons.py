from typing import Union

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Back, Next, Start, Cancel, Group, Row, Button
from aiogram_dialog.widgets.text import Const, Case

from ...states import HelpSG, MainSG


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


async def callback_exit_button(_callback: CallbackQuery, __button: Button, manager: DialogManager):
    stack = manager.current_stack()
    intents = stack.intents

    if len(intents) > 1:
        await manager.done()
    else:
        await manager.start(MainSG.start, mode=StartMode.RESET_STACK)


HELP_BUTTON = Start(Const("Помощь ❓"), id="help", state=HelpSG.help_)
BACK_BUTTON = Back(Const("Назад  ⬅️"), id="back", when=has_back_state)
NEXT_BUTTON = Next(Const("Далее  ➡️"), id="next", when=has_next_state)
EXIT_BUTTON = Cancel(Const("Выйти  🚪"), id="pop_stack", when=has_stack_above)

EXIT_OR_START_BUTTON = Button(Case(
    {
        True: Const("Выйти  🚪"),
        False: Const("Начать  🚪")
    },
    selector=lambda data, widget, manager: len(manager.current_stack().intents) > 1
),
    id="pop_or_start_stack",
    on_click=callback_exit_button
)

NAVIGATION_BAR = Group(Row(BACK_BUTTON), EXIT_BUTTON)




