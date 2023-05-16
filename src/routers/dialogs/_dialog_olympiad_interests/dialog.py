import operator

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo, Group, Column, Multiselect, Button, Cancel
from aiogram_dialog.widgets.text import Const, Format

from routers.dialogs.common_components.buttons import NAVIGATION_BAR, EXIT_OR_START_BUTTON
from routers.states import MainSG
from .callbacks import on_class_changed, on_subject_changed, on_level_changed, get_options, on_start, on_submit

olympiad_interest_window = Window(
    Const("Сейчас я задам тебе несколько вопросов, чтобы понять, какие олимпиады тебе будут интересны."),
    SwitchTo(Const("Начать"), id="start_asking_interests", state=MainSG.Interests.ask_user_for_class),
    EXIT_OR_START_BUTTON,
    state=MainSG.Interests.start
)

class_kbd = Multiselect(
    Format("✅  {item[0]}"),
    Format("⏺️  {item[0]}"),
    id="m_classes",
    item_id_getter=operator.itemgetter(1),
    items="classes_options",
    on_state_changed=on_class_changed,
)

subject_kbd = Multiselect(
    Format(r"<< {item[0]} >>"),
    Format("{item[0]}"),
    id="m_subjects",
    item_id_getter=operator.itemgetter(1),
    items="subjects_options",
    on_state_changed=on_subject_changed,
)
level_kbd = Multiselect(
    Format(r"<< {item[0]} >>"),
    Format("{item[0]}"),
    id="m_levels",
    item_id_getter=operator.itemgetter(1),
    items="levels_options",
    on_state_changed=on_level_changed,
)

ask_for_class_window = Window(
    Const("Какой класс\\курс ты рассматриваешь для участия в олимпиадах?"),
    Group(class_kbd, width=3),
    SwitchTo(Const("Далее  ➡️"), id="ask_for_subjects", state=MainSG.Interests.ask_user_for_subjects),
    NAVIGATION_BAR,
    state=MainSG.Interests.ask_user_for_class,
    getter=get_options
)

ask_for_subjects_window = Window(
    Const("Какие учебные предметы вызывают у тебя наибольший интерес?"),
    Group(subject_kbd, width=2),
    SwitchTo(Const("Далее  ➡️"), id="ask_for_levels", state=MainSG.Interests.ask_user_for_olympiad_level),
    NAVIGATION_BAR,
    state=MainSG.Interests.ask_user_for_subjects,
    getter=get_options,
    parse_mode="HTML"
)

ask_for_levels_window = Window(
    Const("Какого уровня олимпиады были бы для тебя наиболее предпочтительными для участия?"),
    Column(level_kbd),
    Button(Const("Завершить"), id="submit_interests", on_click=on_submit),
    NAVIGATION_BAR,
    state=MainSG.Interests.ask_user_for_olympiad_level,
    getter=get_options,
    preview_add_transitions=None,
    parse_mode="HTML",
)

windows = [olympiad_interest_window, ask_for_class_window, ask_for_subjects_window, ask_for_levels_window]

dialog = Dialog(*windows, on_start=on_start)

__all__ = ["dialog"]
