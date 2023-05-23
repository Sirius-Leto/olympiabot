from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Dialog, StartMode
from aiogram_dialog.widgets.kbd import Multiselect, ManagedMultiSelectAdapter

from .context import InterestContext, InterestOptionsSingleton
from ...states import UserSG


async def on_start(_dialog: Dialog, manager: DialogManager):
    # middeware
    options = InterestOptionsSingleton()
    manager.dialog_data["context"] = InterestContext(options)

    # widgets
    level_kbd = manager.find("m_levels")
    level_kbd: ManagedMultiSelectAdapter

    # set all items to check in level_kbd
    for item in options.levels_options:
        await level_kbd.set_checked(item_id=item[1], checked=True)


async def get_options(dialog_manager: DialogManager, **_kwargs) -> dict:
    context: InterestContext = dialog_manager.dialog_data["context"]
    return context.get_options()


async def on_submit(_callback: CallbackQuery, _widget: Any, manager: DialogManager):
    context: InterestContext = manager.dialog_data["context"]

    grades_kbd = manager.find("m_grades")
    grades_kbd: ManagedMultiSelectAdapter
    levels_kbd = manager.find("m_levels")
    levels_kbd: ManagedMultiSelectAdapter
    subjects_kbd = manager.find("m_subjects")
    subjects_kbd: ManagedMultiSelectAdapter

    # get selected items from keyboards
    grades = grades_kbd.get_checked()
    levels = levels_kbd.get_checked()
    subjects = subjects_kbd.get_checked()

    # set selected items to context
    context.set_chosen("grades", grades)
    context.set_chosen("levels", levels)
    context.set_chosen("subjects", subjects)

    # remove this dialog from stack
    await manager.mark_closed()

    # start next dialog
    await manager.start(UserSG.SearchOlympiads.list_olympiads, data=context.get_result())


__all__ = ["on_start", "get_options", "on_submit"]
