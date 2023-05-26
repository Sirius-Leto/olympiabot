from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Url
from aiogram_dialog.widgets.text import Const, Jinja, Format

from routers.states import UserSG
from .buttons import *
from .callbacks import *
from ..common_components.buttons import HELP_BUTTON, EXIT_OR_START_BUTTON
from ..common_components.emojis import *

menu_window = Window(
    Const(
        "Для поиска олимпиад, пожалуйста, укажи критерии поиска. Ты можешь выбрать предмет, уровень, тип олимпиады "
        "или указать ключевое слово. Если нужна помощь, нажми \"Помощь\"."
    ),
    TO_FILTERS_BUTTON,
    SUBMIT_BUTTON,
    EXIT_OR_START_BUTTON,
    HELP_BUTTON,
    state=UserSG.SearchOlympiads.start
)

filters_window = Window(
    Const("Выбери критерий поиска"),
    filters_kb,
    RESET_BUTTON,
    SUBMIT_BUTTON,
    TO_MENU_BUTTON,
    state=UserSG.SearchOlympiads.filters
)

filter_grades_window = Window(
    Const("Выбери классы"),
    grades_kbd,
    SUBMIT_BUTTON,
    TO_FILTERS_BUTTON,
    state=UserSG.SearchOlympiads.filter_grades,
)

filter_subjects_window = Window(
    Const("Выбери предметы"),
    subject_kbd,
    SUBMIT_BUTTON,
    TO_FILTERS_BUTTON,
    state=UserSG.SearchOlympiads.filter_subjects
)

filter_levels_window = Window(
    Const("Выбери уровни"),
    level_kbd,
    SUBMIT_BUTTON,
    TO_FILTERS_BUTTON,
    state=UserSG.SearchOlympiads.filter_levels
)

list_olympiads_window = Window(
    Const("Список олимпиад по ваших критериям"),
    list_kb,
    TO_FILTERS_BUTTON,
    TO_MENU_BUTTON,
    state=UserSG.SearchOlympiads.list_olympiads,
    getter=olympiads_getter
)

jinja_template_for_olympiad = Jinja("""
<b>{{event.name}}</b>

{% if event.begin_date %}
Начало: <i>{{event.begin_date.strftime("%d.%m.%Y")}}</i>
{% endif %}
{% if event.end_date %}
Окончание: <i>{{event.end_date.strftime("%d.%m.%Y")}}</i>

{% endif %}
———————————————————————————————
{# subjects: <code>Математика</code> <code>Физика</code> <code>Информатика</code> #}
{% if event.subjects %}

📚 <b>Предметы</b>
{% for subject in event.subjects %}
<code>[{{subject.name}}]</code> {% endfor %}

{% endif %}

{% if event.grades %}
👨‍🎓 <b>Для {{ event.get_grades_display() }} классов </b>
{% endif %}

{% if event.levels %}
📈 <b>Уровни</b>
{% for level in event.levels %}
[{{level.description}}] {% endfor %}

{% endif %}

{% if event.format %}
<b>Формат проведения</b>
{{event.format}}
{% endif %}

{% if event.description %}
<b>Описание</b>
{{event.description}}
{% endif %}

{% if event.tags %}
<b>Теги</b>
{% for tag in event.tags %}
———————————————————————————————
<i>{{tag.name}}</i>
{{tag.description}} 
{% endfor %}
{% endif %}
""")

show_olympiad_window = Window(
    jinja_template_for_olympiad,
    Url(
        Const(LINK_EMOJI + " Подробнее"),
        Format("{event.url}"),
        id="event_url",
        when=lambda data, _button, _manager: data.get("event").url
    ),
    TO_LIST_BUTTON,
    TO_FILTERS_BUTTON,
    parse_mode="HTML",
    state=UserSG.SearchOlympiads.show_olympiad,
    getter=olympiad_getter
)

windows = [filters_window,
           filter_subjects_window,
           filter_levels_window,
           filter_grades_window,
           menu_window,
           list_olympiads_window,
           show_olympiad_window]

dialog = Dialog(*windows, on_start=on_start, getter=get_options)

__all__ = ["dialog"]
