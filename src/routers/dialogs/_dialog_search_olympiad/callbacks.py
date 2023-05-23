from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Dialog
from aiogram_dialog.api.internal import Widget
from aiogram_dialog.widgets.kbd import ManagedMultiSelectAdapter

from data.repositories.olympiads import AbstractOlympiadsRepository
from routers.dialogs._dialog_search_olympiad.context import FilterContext, FilterOptionsSingleton
from routers.states import UserSG


async def on_start(_dialog: Dialog, dialog_manager: DialogManager):
    options = FilterOptionsSingleton(dialog_manager.middleware_data["olympiads_repository"])
    await options.init()
    context = FilterContext(options)
    dialog_manager.dialog_data["context"] = context

    if dialog_manager.start_data:
        if "grades" in dialog_manager.start_data:
            grades_kbd = dialog_manager.find("m_grades")
            grades_kbd: ManagedMultiSelectAdapter
            for item in dialog_manager.start_data["grades"]:
                await grades_kbd.set_checked(item_id=item, checked=True)

        if "levels" in dialog_manager.start_data:
            levels_kbd = dialog_manager.find("m_levels")
            levels_kbd: ManagedMultiSelectAdapter
            for item in dialog_manager.start_data["levels"]:
                await levels_kbd.set_checked(item_id=item, checked=True)

        if "subjects" in dialog_manager.start_data:
            subjects_kbd = dialog_manager.find("m_subjects")
            subjects_kbd: ManagedMultiSelectAdapter
            for item in dialog_manager.start_data["subjects"]:
                await subjects_kbd.set_checked(item_id=item, checked=True)

        await update_filters(dialog_manager)
        events = await dialog_manager.middleware_data["olympiads_repository"].filter_olympiads(**context.get_result())
        context.filtered_olympiads = events


async def get_options(dialog_manager: DialogManager, **_kwargs) -> dict:
    context: FilterContext = dialog_manager.dialog_data["context"]
    return context.get_options()


async def update_filters(dialog_manager: DialogManager):
    context: FilterContext = dialog_manager.dialog_data["context"]

    grades: ManagedMultiSelectAdapter = dialog_manager.find("m_grades")
    levels: ManagedMultiSelectAdapter = dialog_manager.find("m_levels")
    subjects: ManagedMultiSelectAdapter = dialog_manager.find("m_subjects")

    # set selected items to context
    if grades:
        context.set_chosen("grades", grades.get_checked())
    if levels:
        context.set_chosen("levels", levels.get_checked())
    if subjects:
        context.set_chosen("subjects", subjects.get_checked())


# noinspection PydanticTypeChecker
async def on_submit(_callback: CallbackQuery, _widget: Widget, dialog_manager: DialogManager):
    await update_filters(dialog_manager)

    context: FilterContext = dialog_manager.dialog_data["context"]
    events = await dialog_manager.middleware_data["olympiads_repository"].filter_olympiads(**context.get_result())
    context.filtered_olympiads = events

    await dialog_manager.switch_to(UserSG.SearchOlympiads.list_olympiads)


async def olympiads_getter(dialog_manager: DialogManager, **_kwargs) -> dict[str, ...]:
    context: FilterContext = dialog_manager.dialog_data["context"]
    return {"olympiads": context.filtered_olympiads}


async def on_reset(_callback: CallbackQuery, _widget: Widget, dialog_manager: DialogManager):
    # remove all selected items from widgets
    subjects: ManagedMultiSelectAdapter = dialog_manager.find("m_subjects")
    levels: ManagedMultiSelectAdapter = dialog_manager.find("m_levels")
    grades: ManagedMultiSelectAdapter = dialog_manager.find("m_grades")

    if subjects:
        await subjects.reset_checked()

    if levels:
        await levels.reset_checked()

    if grades:
        await grades.reset_checked()


async def on_olympiad_click(_c: CallbackQuery, _widget: Any, dialog_manager: DialogManager, item_id: str):
    # item_id is id in the database
    repository: AbstractOlympiadsRepository = dialog_manager.middleware_data["olympiads_repository"]
    event = await repository.get_event(int(item_id))
    context: FilterContext = dialog_manager.dialog_data["context"]
    context.chosen_olympiad = event
    await dialog_manager.switch_to(UserSG.SearchOlympiads.show_olympiad)


async def olympiad_getter(dialog_manager: DialogManager, **_kwargs) -> dict[str, ...]:
    context: FilterContext = dialog_manager.dialog_data["context"]
    return {"event": context.chosen_olympiad}


__all__ = ["on_start", "get_options", "on_submit", "on_olympiad_click", "olympiads_getter", "on_reset",
           "olympiad_getter"]
