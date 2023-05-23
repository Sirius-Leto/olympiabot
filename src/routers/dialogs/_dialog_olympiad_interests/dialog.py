import operator

from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import SwitchTo, Group, Column, Multiselect, Button
from aiogram_dialog.widgets.text import Const, Format

from routers.states import UserSG
from .callbacks import *
from ..common_components.buttons import NAVIGATION_BAR, EXIT_OR_START_BUTTON
from ..common_components.emojis import OK_EMOJI, EMPTY_EMOJI, NEXT_EMOJI, SUBMIT_EMOJI

olympiad_interest_window = Window(
    Const("Сейчас я задам тебе несколько вопросов, чтобы понять, какие олимпиады тебе будут интересны."),
    SwitchTo(Const("Начать"), id="start_asking_interests", state=UserSG.Interests.ask_grades),
    EXIT_OR_START_BUTTON,
    state=UserSG.Interests.start
)

grade_kbd = Multiselect(
    Format(OK_EMOJI + "  {item[0]}"),
    Format(EMPTY_EMOJI + "  {item[0]}"),
    id="m_grades",
    item_id_getter=operator.itemgetter(1),
    items="grades_options",
)

subject_kbd = Multiselect(
    Format(r"<< {item[0]} >>"),
    Format("{item[0]}"),
    id="m_subjects",
    item_id_getter=operator.itemgetter(1),
    items="subjects_options",
)
level_kbd = Multiselect(
    Format(r"<< {item[0]} >>"),
    Format("{item[0]}"),
    id="m_levels",
    item_id_getter=operator.itemgetter(1),
    items="levels_options",
)

ask_for_grade_window = Window(
    Const("Какой класс\\курс ты рассматриваешь для участия в олимпиадах?"),
    Group(grade_kbd, width=3),
    SwitchTo(Const("Далее  " + NEXT_EMOJI), id="ask_for_subjects", state=UserSG.Interests.ask_subjects),
    NAVIGATION_BAR,
    state=UserSG.Interests.ask_grades
)

ask_for_subjects_window = Window(
    Const("Какие учебные предметы вызывают у тебя наибольший интерес?"),
    Group(subject_kbd, width=2),
    SwitchTo(Const("Далее  " + NEXT_EMOJI), id="ask_for_levels", state=UserSG.Interests.ask_levels),
    NAVIGATION_BAR,
    state=UserSG.Interests.ask_subjects,
    parse_mode="HTML"
)

ask_for_levels_window = Window(
    Const("Какого уровня олимпиады были бы для тебя наиболее предпочтительными для участия?"),
    Column(level_kbd),
    Button(Const("Завершить  " + SUBMIT_EMOJI), id="submit_interests", on_click=on_submit),
    NAVIGATION_BAR,
    state=UserSG.Interests.ask_levels,
    preview_add_transitions=None,
    parse_mode="HTML",
)

windows = [olympiad_interest_window, ask_for_grade_window, ask_for_subjects_window, ask_for_levels_window]

dialog = Dialog(*windows, on_start=on_start, getter=get_options)
