from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Dialog

from .context import InterestContext


async def on_start(_dialog: Dialog, manager: DialogManager):
    manager.dialog_data["context"] = InterestContext()


async def get_options(dialog_manager: DialogManager, **_kwargs) -> dict:
    context: InterestContext = dialog_manager.dialog_data["context"]
    return context.get_options()


async def on_class_changed(_callback: CallbackQuery, widget: Any,
                           _manager: DialogManager, item_id: str):
    is_checked = widget.is_checked(item_id)
    context: InterestContext = _manager.dialog_data["context"]

    if is_checked:
        context.add_chosen("classes", item_id)
    else:
        context.remove_chosen("classes", item_id)


async def on_subject_changed(_callback: CallbackQuery, widget: Any,
                             _manager: DialogManager, item_id: str):
    is_checked = widget.is_checked(item_id)
    context: InterestContext = _manager.dialog_data["context"]

    if is_checked:
        context.add_chosen("subjects", item_id)
    else:
        context.remove_chosen("subjects", item_id)


async def on_level_changed(_callback: CallbackQuery, widget: Any,
                           _manager: DialogManager, item_id: str):
    is_checked = widget.is_checked(item_id)
    context: InterestContext = _manager.dialog_data["context"]

    if is_checked:
        context.add_chosen("levels", item_id)
    else:
        context.remove_chosen("levels", item_id)


async def on_submit(_callback: CallbackQuery, _widget: Any, manager: DialogManager):
    context: InterestContext = manager.dialog_data["context"]
    await manager.done(result=context.get_result())
