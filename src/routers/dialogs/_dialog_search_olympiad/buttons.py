import operator

from aiogram_dialog.widgets.kbd import Button, SwitchTo, Group, Multiselect, ScrollingGroup, Column, Select
from aiogram_dialog.widgets.text import Const, Format

from routers.states import UserSG
from .callbacks import *
from ..common_components.emojis import *

SUBMIT_BUTTON = Button(Const("Найти олимпиады  " + SEARCH_EMOJI), id="submit", on_click=on_submit)

TO_FILTERS_BUTTON = SwitchTo(Const("Критерии поиска  " + FILTERS_EMOJI), id="to_filters",
                             state=UserSG.SearchOlympiads.filters)

TO_MENU_BUTTON = SwitchTo(Const("Вернуться в меню  " + BACK_EMOJI), id="to_menu", state=UserSG.SearchOlympiads.start)

RESET_BUTTON = Button(Const("Сбросить  " + RESET_EMOJI), id="reset", on_click=on_reset)

TO_LIST_BUTTON = SwitchTo(Const("К списку олимпиад"), id="list_olympiads", state=UserSG.SearchOlympiads.list_olympiads)

grades_kbd = Group(Multiselect(
    Format("<< {item[0]} >>"),
    Format("{item[0]}"),
    id="m_grades",
    item_id_getter=operator.itemgetter(1),
    items="grades_options",
),
    id="grades_kbd",
    width=3
)

subject_kbd = ScrollingGroup(Multiselect(
    Format(r"<< {item[0]} >>"),
    Format("{item[0]}"),
    id="m_subjects",
    item_id_getter=operator.itemgetter(1),
    items="subjects_options",
),
    id="subject_kbd",
    height=7,
    width=2,
)

level_kbd = Group(Multiselect(
    Format(r"<< {item[0]} >>"),
    Format("{item[0]}"),
    id="m_levels",
    item_id_getter=operator.itemgetter(1),
    items="levels_options",
),
    id="level_kbd",
    width=1
)

filters_kb = Group(
    Column(
        # SwitchTo(Const(FILTER_NAME_EMOJI + "  Название"),
        #          id="name",
        #          state=UserSG.SearchOlympiads.filter_name),
        SwitchTo(Const(FILTER_SUBJECTS_EMOJI + "  Предмет"),
                 id="subject",
                 state=UserSG.SearchOlympiads.filter_subjects),
        SwitchTo(Const(FILTER_LEVELS_EMOJI + "  Уровень"),
                 id="level",
                 state=UserSG.SearchOlympiads.filter_levels),
        SwitchTo(Const(FILTER_GRADES_EMOJI + "  Класс участия"),
                 id="grade",
                 state=UserSG.SearchOlympiads.filter_grades),
        # SwitchTo(Const(FILTER_BY_DATE_EMOJI + "  Дата проведения"),
        #          id="time",
        #          state=UserSG.SearchOlympiads.filter_by_date),
    ),
    id="filters_kb",
)

list_kb = ScrollingGroup(
    Select(
        Format("{item[0]}"),
        id="olympiad",
        item_id_getter=operator.itemgetter(1),
        items="olympiads",
        on_click=on_olympiad_click,
    ),

    id="list_kb",
    height=7,
    width=1,
)

__all__ = ["SUBMIT_BUTTON", "TO_FILTERS_BUTTON", "TO_MENU_BUTTON", "RESET_BUTTON", "TO_LIST_BUTTON",
           "grades_kbd", "subject_kbd", "level_kbd", "filters_kb", "list_kb"]
