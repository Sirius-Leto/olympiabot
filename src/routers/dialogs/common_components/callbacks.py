from typing import Union

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Button

from routers.states import UserSG


async def callback_exit_or_start_button(_callback: CallbackQuery, __button: Button, manager: DialogManager):
    stack = manager.current_stack()
    intents = stack.intents

    if len(intents) > 1:
        await manager.done()
    else:
        await manager.start(UserSG.start, mode=StartMode.RESET_STACK)


async def callback_exit_button(_callback: CallbackQuery, __button: Button, manager: DialogManager):
    await manager.done()


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


__all__ = ["callback_exit_or_start_button", "callback_exit_button", "has_stack_above", "has_back_state",
           "has_next_state"]
